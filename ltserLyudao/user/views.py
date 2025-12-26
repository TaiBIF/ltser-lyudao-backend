from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    Contact,
    Literature,
    QATag,
    QuestionAnswer,
    FormLink,
    FormLinkAttachment,
    NewsTag,
    News,
    MyUser,
    NewsImage,
    NewsAttachment,
    NewsCoverImage,
    About,
    AboutAttachment,
    DownloadRecord,
    DownloadApply,
    SocialEconomyVisitors,
)
from .serializers import (
    ContactSerializer,
    LiteratureSerializer,
    RegisterSerializer,
    QATagSerializer,
    QuestionAnswerSerializer,
    FormLinkSerializer,
    NewsTagSerializer,
    NewsSerializer,
    NewsDetailSerializer,
    EmailVerificationSerializer,
    ResendEmailVerifySerializer,
    LoginSerializer,
    UpdatePasswordSerializer,
    ResetPasswordEmailRequestSerializer,
    SetNewPasswordSerializer,
    AboutSerializer,
    AboutPostPatchSerializer,
    DownloadRecordSerializer,
    DownloadApplySerializer,
    AboutAttachmentSerializer,
    AboutDetailSerializer,
    MyUserSerializer,
    SocialEconomyVisitorsSerializer,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination
from django.db import transaction
import zipfile
import os
import io
from django.http import FileResponse
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
import jwt
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.provider import GoogleProvider
import logging

logger = logging.getLogger(__name__)
import requests
import secrets


class GoogleAuthAPIView(APIView):
    permission_classes = [AllowAny]

    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    REDIRECT_URI = "https://ltsertwlyudao.org"
    TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
    USER_INFO_ENDPOINT = "https://www.googleapis.com/oauth2/v3/userinfo"

    def post(self, request):
        authorization_code = request.data.get("authorization_code")
        if not authorization_code:
            return Response(
                {"message": "Authorization code is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Exchange authorization_code for access_token
            payload = {
                "client_id": self.CLIENT_ID,
                "client_secret": self.CLIENT_SECRET,
                "redirect_uri": self.REDIRECT_URI,
                "grant_type": "authorization_code",
                "code": authorization_code,
            }

            response = requests.post(self.TOKEN_ENDPOINT, data=payload)
            token_info = response.json()

            if not token_info.get("access_token"):
                raise Exception("Failed to get access token from Google")

            # Use the access_token to get user info from Google
            headers = {"Authorization": f"Bearer {token_info['access_token']}"}
            response = requests.get(self.USER_INFO_ENDPOINT, headers=headers)
            user_info = response.json()

            defaults = {
                "username": user_info["email"],
                "first_name": user_info.get("given_name", ""),
                "last_name": user_info.get("family_name", ""),
                "is_verified": True,
                "is_regular_user": True,
            }
            user, created = MyUser.objects.get_or_create(
                email=user_info["email"], defaults=defaults
            )

            if created or not user.password:
                fake_password = secrets.token_hex(16)  # 生成一個隨機密碼
                user.set_password(fake_password)
                user.save()

            social_account, created = SocialAccount.objects.get_or_create(
                provider=GoogleProvider.id,
                uid=user_info["sub"],
                defaults={"user": user, "extra_data": user_info},
            )

            if not created:
                social_account.extra_data = user_info
                social_account.save(update_fields=["extra_data"])

            refresh = RefreshToken.for_user(user)
            token_data = {"refresh": str(refresh), "access": str(refresh.access_token)}

            return Response(token_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10


class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        userData = serializer.data
        user = MyUser.objects.get(email=userData["email"])
        token = RefreshToken.for_user(user).access_token
        absurl = f"https://ltsertwlyudao.org/verify-email/?token={str(token)}"
        data = {
            "url": absurl,
            "toEmail": user.email,
            "emailSubject": "LTSER LYUDAO會員註冊驗證",
        }
        Util.send_mail("email_template.html", data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmailAPIView(APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(str(token), settings.SECRET_KEY, "HS256")
            user = MyUser.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({"email": "使用者成功驗證帳號"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {"error": "Activation Expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as identifier:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class ResendEmailVerifyAPIView(APIView):
    serializer_class = ResendEmailVerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        try:
            user = MyUser.objects.get(email=email)
            if user.is_verified:
                return Response(
                    {"message": "使用者已被激活"}, status=status.HTTP_409_CONFLICT
                )
            else:
                token = RefreshToken.for_user(user).access_token
                absurl = f"https://ltsertwlyudao.org/verify-email/?token={str(token)}"
                data = {
                    "url": absurl,
                    "toEmail": user.email,
                    "emailSubject": "LTSER LYUDAO會員註冊驗證",
                }
                Util.send_mail("email_template.html", data)
                return Response(
                    {"message": "已重新發送驗證信"}, status=status.HTTP_200_OK
                )
        except ObjectDoesNotExist:
            return Response(
                {"message": "使用者不存在"}, status=status.HTTP_404_NOT_FOUND
            )


class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MemberInformationAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = MyUser.objects.get(id=request.user.id)
            serializer = MyUserSerializer(user)
            return Response(serializer.data)
        except MyUser.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request):
        try:
            user = MyUser.objects.get(id=request.user.id)
            serializer = MyUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MyUser.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class UpdateUserPasswordAPIView(APIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not user.check_password(request.data["oldPassword"]):
                return Response(
                    {"message": "舊密碼錯誤"}, status=status.HTTP_400_BAD_REQUEST
                )

            if request.data["newPassword"] != request.data["newPassword2"]:
                return Response(
                    {"message": "密碼確認錯誤"}, status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(request.data["newPassword"])
            user.save()
            data = {
                "toEmail": user.email,
                "emailSubject": "LTSER LYUDAO會員更新密碼",
            }
            Util.send_mail("password_update_template.html", data)
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "更新密碼成功",
            }

            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmailAPIView(APIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        # 先確保資料的有效性
        if not serializer.is_valid():
            return Response(
                {"status": "error", "message": "無效的輸入"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = request.data["email"]

        if MyUser.objects.filter(email=email).exists():
            user = MyUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            absurl = f"https://ltsertwlyudao.org/reset-password/?uidb64={str(uidb64)}&token={str(token)}"
            data = {
                "url": absurl,
                "toEmail": user.email,
                "emailSubject": "LTSER LYUDAO會員忘記密碼通知信",
            }
            Util.send_mail("password_reset_template.html", data)
            return Response(
                {"status": "success", "message": "已經寄出連結，請使用連結重置密碼"},
                status=status.HTTP_200_OK,
            )
        else:
            # 使用者不存在
            return Response(
                {"message": "您尚未註冊"}, status=status.HTTP_400_BAD_REQUEST
            )


class PasswordTokenCheckAPIView(APIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = MyUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"error": "Token is not valid, please request a new one"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            return Response(
                {
                    "success": True,
                    "message": "Credentials Valid",
                    "uidb64": uidb64,
                    "token": token,
                },
                status=status.HTTP_200_OK,
            )
        except DjangoUnicodeDecodeError as identifier:
            return Response(
                {"error": "Token is not valid, please request a new one"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class SetNewPasswordAPIView(APIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": True, "message": "重置密碼成功"}, status=status.HTTP_200_OK
        )


class UserIdentityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.is_superuser:
            return Response({"group": "superuser"}, status=status.HTTP_200_OK)
        elif user.is_social_project_staff:
            return Response(
                {"group": "social_project_staff"}, status=status.HTTP_200_OK
            )
        elif user.is_staff:
            return Response({"group": "staff"}, status=status.HTTP_200_OK)
        else:
            return Response({"group": "none"}, status=status.HTTP_200_OK)


class ContactAPIView(APIView):
    def get(self, request):
        contact_id = request.query_params.get("id")
        if contact_id is not None:
            contact = Contact.objects.get(id=contact_id)
            serializer = ContactSerializer(contact)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            paginator = CustomPageNumberPagination()
            contacts = Contact.objects.all().order_by("id")
            result_page = paginator.paginate_queryset(contacts, request)
            serializer = ContactSerializer(result_page, many=True)
            return Response(
                {
                    "currentPage": paginator.page.number,
                    "recordsPerPage": paginator.page_size,
                    "totalPages": paginator.page.paginator.num_pages,
                    "totalRecords": paginator.page.paginator.count,
                    "records": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

    @swagger_auto_schema(request_body=ContactSerializer)
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ContactSerializer)
    def patch(self, request):
        contact_id = request.query_params.get("id")
        contact = Contact.objects.get(id=contact_id)
        serializer = ContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            if "image" in request.data:
                contact.image.delete()
                contact.image = request.data["image"]
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        contact_id = request.query_params.get("id")
        contact = Contact.objects.get(id=contact_id)
        contact.delete()
        response_data = {"message": "刪除成功"}
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


class ContactAllAPIView(APIView):
    def get(self, request):
        language = request.headers.get("Ltser-User-Language", "zh-tw")
        contacts = Contact.objects.all().order_by("id")
        serializer = ContactSerializer(contacts, many=True)
        modified_data = []
        for contact in serializer.data:
            if language.lower() == "en":
                contact["content"] = contact.get("content_en")
                contact["name"] = contact.get("name_en")
                contact["unit"] = contact.get("unit_en")

            contact.pop("content_en", None)
            contact.pop("name_en", None)
            contact.pop("unit_en", None)

            modified_data.append(contact)

        return Response(modified_data, status=status.HTTP_200_OK)


class LiteratureAPIView(APIView):

    def get(self, request):
        literature_id = request.query_params.get("id")
        keyword = request.query_params.get("keyword")
        category = request.query_params.get("category")
        relate = request.query_params.get("relate")
        year = request.query_params.get("year")
        if literature_id is not None:
            literature = Literature.objects.get(id=literature_id)
            serializer = LiteratureSerializer(literature)
            return Response(serializer.data, status=status.HTTP_200_OK)

        literature = Literature.objects.all()

        if keyword:
            literature = literature.filter(title__icontains=keyword)

        if category:
            literature = literature.filter(category__iexact=category)

        if relate:
            literature = literature.filter(relate__iexact=relate)

        if year:
            literature = literature.filter(year=year)

        literature = literature.order_by("-year")

        paginator = CustomPageNumberPagination()
        result_page = paginator.paginate_queryset(literature, request)
        serializer = LiteratureSerializer(result_page, many=True)
        return Response(
            {
                "currentPage": paginator.page.number,
                "recordsPerPage": paginator.page_size,
                "totalPages": paginator.page.paginator.num_pages,
                "totalRecords": paginator.page.paginator.count,
                "records": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(request_body=LiteratureSerializer)
    def post(self, request):
        serializer = LiteratureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=LiteratureSerializer)
    def patch(self, request):
        literature_id = request.query_params.get("id")
        literature = Literature.objects.get(id=literature_id)
        serializer = LiteratureSerializer(literature, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        literature_id = request.query_params.get("id")
        literature = Literature.objects.get(id=literature_id)
        literature.delete()
        response_data = {"message": "刪除成功"}
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


class QATagAPIView(APIView):
    def get(self, request):
        tag_id = request.query_params.get("id")
        if tag_id is not None:
            tag = QATag.objects.get(id=tag_id)
            serializer = QATagSerializer(tag, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            paginator = CustomPageNumberPagination()
            tags = QATag.objects.all().order_by("id")
            result_page = paginator.paginate_queryset(tags, request)
            serializer = QATagSerializer(
                result_page, many=True, context={"request": request}
            )
            return Response(
                {
                    "currentPage": paginator.page.number,
                    "recordsPerPage": paginator.page_size,
                    "totalPages": paginator.page.paginator.num_pages,
                    "totalRecords": paginator.page.paginator.count,
                    "records": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

    @swagger_auto_schema(request_body=QATagSerializer)
    def post(self, request):
        serializer = QATagSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=QATagSerializer)
    def patch(self, request):
        tag_id = request.query_params.get("id")
        tag = QATag.objects.get(id=tag_id)
        serializer = QATagSerializer(
            tag, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        tag_id = request.query_params.get("id")
        tag = QATag.objects.get(id=tag_id)
        tag.delete()
        response_data = {"message": "刪除成功"}
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


class QuestionAnswerAPIView(APIView):
    def get(self, request):
        question_answer_id = request.query_params.get("id")
        tag_id = request.query_params.get("tag")
        if question_answer_id is not None:
            question_answer = QuestionAnswer.objects.get(id=question_answer_id)
            serializer = QuestionAnswerSerializer(
                question_answer, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif tag_id is not None:
            # 返回特定標籤的新聞
            try:
                question_answer = QuestionAnswer.objects.filter(
                    type__id=tag_id
                ).order_by("-id")
                paginator = CustomPageNumberPagination()
                result_page = paginator.paginate_queryset(question_answer, request)
                serializer = QuestionAnswerSerializer(
                    result_page, many=True, context={"request": request}
                )
                return Response(
                    {
                        "currentPage": paginator.page.number,
                        "recordsPerPage": paginator.page_size,
                        "totalPages": paginator.page.paginator.num_pages,
                        "totalRecords": paginator.page.paginator.count,
                        "records": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            except QuestionAnswer.DoesNotExist:
                return Response(
                    {"message": "News not found."}, status=status.HTTP_404_NOT_FOUND
                )

        else:
            paginator = CustomPageNumberPagination()
            question_answers = QuestionAnswer.objects.all().order_by("-id")
            result_page = paginator.paginate_queryset(question_answers, request)
            serializer = QuestionAnswerSerializer(
                result_page, many=True, context={"request": request}
            )
            return Response(
                {
                    "currentPage": paginator.page.number,
                    "recordsPerPage": paginator.page_size,
                    "totalPages": paginator.page.paginator.num_pages,
                    "totalRecords": paginator.page.paginator.count,
                    "records": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

    @swagger_auto_schema(request_body=QuestionAnswerSerializer)
    def post(self, request):
        serializer = QuestionAnswerSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=QuestionAnswerSerializer)
    def patch(self, request):
        question_answer_id = request.query_params.get("id")
        if question_answer_id is not None:
            question_answer = QuestionAnswer.objects.get(id=question_answer_id)
            serializer = QuestionAnswerSerializer(
                question_answer,
                data=request.data,
                partial=True,
                context={"request": request},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"message": "請提供有效的id"}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):
        question_answer_id = request.query_params.get("id")
        if question_answer_id is not None:
            question_answer = QuestionAnswer.objects.get(id=question_answer_id)
            question_answer.delete()
            response_data = {"message": "刪除成功"}
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"message": "請提供有效的id"}, status=status.HTTP_400_BAD_REQUEST
            )


class FormLinkAPIVIew(APIView):
    def get(self, request):
        formlink_id = request.query_params.get("id")
        if formlink_id is not None:
            formlink = FormLink.objects.get(id=formlink_id)
            serializer = FormLinkSerializer(formlink)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            paginator = CustomPageNumberPagination()
            formlink = FormLink.objects.all().order_by("id")
            result_page = paginator.paginate_queryset(formlink, request)
            serializer = FormLinkSerializer(result_page, many=True)
            return Response(
                {
                    "currentPage": paginator.page.number,
                    "recordsPerPage": paginator.page_size,
                    "totalPages": paginator.page.paginator.num_pages,
                    "totalRecords": paginator.page.paginator.count,
                    "records": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

    def post(self, request):
        name = request.data.get("name")
        link = request.data.get("link")
        files = request.FILES.getlist("files")

        with transaction.atomic():
            try:
                form_link = FormLink.objects.create(name=name, link=link)

                for file in files:
                    FormLinkAttachment.objects.create(form_link=form_link, file=file)

                return Response({"message": "新增成功"}, status=status.HTTP_201_CREATED)

            except Exception as e:
                # 回滾事務，如果有任何錯誤發生
                transaction.set_rollback(True)
                return Response(
                    {"message": "新增失敗"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

    def patch(self, request):
        formlink_id = request.query_params.get("id")
        new_name = request.data.get("name", None)
        new_link = request.data.get("link", None)
        new_files = request.FILES.getlist("files")

        if formlink_id is not None:
            with transaction.atomic():
                try:
                    form_link = FormLink.objects.get(id=formlink_id)
                    if new_name is not None:
                        form_link.name = new_name
                    if new_link is not None:
                        form_link.link = new_link
                    form_link.save()
                    FormLinkAttachment.objects.filter(form_link=form_link).delete()

                    for file in new_files:
                        FormLinkAttachment.objects.create(
                            form_link=form_link, file=file
                        )
                    return Response({"message": "更新成功"}, status=status.HTTP_200_OK)

                except Exception as e:
                    transaction.set_rollback(True)
                    return Response(
                        {"message": "更新失敗"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
        else:
            return Response(
                {"message": "錯誤的 id"}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):
        formlink_id = request.query_params.get("id")
        if formlink_id is not None:
            formlink = FormLink.objects.get(id=formlink_id)
            formlink.delete()
            response_data = {"message": "刪除成功"}
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"message": "請提供有效的id"}, status=status.HTTP_400_BAD_REQUEST
            )


class FormLinkDownloadAPIview(APIView):
    def get(self, request):
        formlink_id = request.GET.get("id")
        try:
            form_link = FormLink.objects.get(pk=formlink_id)
        except FormLink.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        attachments = form_link.formLinkAttachments.all()

        if not attachments:
            return Response(
                {"message": "No attachments found for this FormLink"},
                status=status.HTTP_404_NOT_FOUND,
            )

        zip_io = io.BytesIO()
        with zipfile.ZipFile(zip_io, "w", zipfile.ZIP_DEFLATED) as zipf:
            for attachment in attachments:
                # Add each file to the zip file
                zipf.write(
                    attachment.file.path, arcname=os.path.basename(attachment.file.name)
                )

        # Reset file pointer to start
        zip_io.seek(0)

        # Create a FileResponse to send the zip file
        response = FileResponse(zip_io, as_attachment=True, filename="attachments.zip")

        return response


class NewsTagAPIView(APIView):
    def get(self, request):
        tag_id = request.query_params.get("id")
        if tag_id is not None:
            tag = NewsTag.objects.get(id=tag_id)
            serializer = NewsTagSerializer(tag)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            paginator = CustomPageNumberPagination()
            tags = NewsTag.objects.all().order_by("id")
            result_page = paginator.paginate_queryset(tags, request)
            serializer = NewsTagSerializer(result_page, many=True)
            return Response(
                {
                    "currentPage": paginator.page.number,
                    "recordsPerPage": paginator.page_size,
                    "totalPages": paginator.page.paginator.num_pages,
                    "totalRecords": paginator.page.paginator.count,
                    "records": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

    @swagger_auto_schema(request_body=NewsTagSerializer)
    def post(self, request):
        serializer = NewsTagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=NewsTagSerializer)
    def patch(self, request):
        tag_id = request.query_params.get("id")
        tag = NewsTag.objects.get(id=tag_id)
        serializer = NewsTagSerializer(tag, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        tag_id = request.query_params.get("id")
        tag = NewsTag.objects.get(id=tag_id)
        tag.delete()
        response_data = {"message": "刪除成功"}
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)


class NewsAPIView(APIView):
    def get(self, request):
        news_id = request.query_params.get("id")
        tag_id = request.query_params.get("tag")
        startDate = request.query_params.get("startDate")
        endDate = request.query_params.get("endDate")

        if startDate is not None and endDate is not None:
            try:
                startDate = datetime.strptime(startDate, "%Y-%m-%d")
                endDate = datetime.strptime(endDate, "%Y-%m-%d")
            except ValueError:
                return Response(
                    {"message": "Invalid date format. Expected YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if endDate < startDate:
                return Response(
                    {"message": "End date cannot be earlier than start date."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if news_id is not None:
            try:
                news = News.objects.get(id=news_id)
                serializer = NewsDetailSerializer(news)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response(
                    {"message": "News not found."}, status=status.HTTP_404_NOT_FOUND
                )
        elif tag_id is not None:
            try:
                if startDate is not None and endDate is not None:
                    news = News.objects.filter(
                        type__id=tag_id, newsDate__range=(startDate, endDate)
                    ).order_by("-newsDate")
                else:
                    news = News.objects.filter(type__id=tag_id).order_by("-newsDate")
                paginator = CustomPageNumberPagination()
                result_page = paginator.paginate_queryset(news, request)
                serializer = NewsSerializer(result_page, many=True)
                return Response(
                    {
                        "currentPage": paginator.page.number,
                        "recordsPerPage": paginator.page_size,
                        "totalPages": paginator.page.paginator.num_pages,
                        "totalRecords": paginator.page.paginator.count,
                        "records": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            except ObjectDoesNotExist:
                return Response(
                    {"message": "News not found."}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            paginator = CustomPageNumberPagination()
            if startDate is not None and endDate is not None:
                news = News.objects.filter(
                    newsDate__range=(startDate, endDate)
                ).order_by("-newsDate")
            else:
                news = News.objects.all().order_by("-newsDate")
            result_page = paginator.paginate_queryset(news, request)
            serializer = NewsSerializer(result_page, many=True)
            return Response(
                {
                    "currentPage": paginator.page.number,
                    "recordsPerPage": paginator.page_size,
                    "totalPages": paginator.page.paginator.num_pages,
                    "totalRecords": paginator.page.paginator.count,
                    "records": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

    def post(self, request):
        type_ids = request.data.getlist("type")
        user_id = request.data.get("user")
        title = request.data.get("title")
        content = request.data.get("content")
        news_date = request.data.get("newsDate")
        cover_image_file = request.FILES.get("cover")
        images = request.FILES.getlist("images")
        news_attachments = request.FILES.getlist("files")

        with transaction.atomic():
            try:
                # create user instance
                user = MyUser.objects.get(id=user_id)
                # create news instance
                news = News.objects.create(
                    title=title,
                    content=content,
                    newsDate=news_date,
                    user=user,
                )

                cover_image = NewsCoverImage.objects.create(
                    news=news, image=cover_image_file
                )

                news.cover_image = cover_image
                news.save()

                news.type.add(*type_ids)

                for image in images:
                    NewsImage.objects.create(news=news, image=image)

                for attachment in news_attachments:
                    NewsAttachment.objects.create(news=news, file=attachment)

                return Response(
                    {"message": "新聞創建成功"}, status=status.HTTP_201_CREATED
                )

            except Exception as e:
                # rollback transaction if any error occurs
                transaction.set_rollback(True)
                return Response(
                    {"message": "Error occurred while creating news. " + str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

    def patch(self, request):
        news_id = request.query_params.get("id")
        new_title = request.data.get("title", None)
        new_content = request.data.get("content", None)
        new_newsDate = request.data.get("newsDate", None)
        new_type = request.data.getlist("type")
        new_user = request.data.get("user", None)
        new_images = request.FILES.getlist("images")
        new_attachments = request.FILES.getlist("files")
        new_cover_image_file = request.FILES.get("cover")

        if news_id is not None:
            with transaction.atomic():
                try:
                    news = News.objects.get(id=news_id)

                    if new_title is not None:
                        news.title = new_title
                    if new_content is not None:
                        news.content = new_content
                    if new_newsDate is not None:
                        news.newsDate = new_newsDate
                    if new_user is not None:
                        news.user = MyUser.objects.get(id=new_user)

                    # Check if a cover image is provided and a previous one exists
                    if (
                        new_cover_image_file is not None
                        and news.cover_image is not None
                    ):
                        news.cover_image.image = new_cover_image_file
                        news.cover_image.save()

                    news.save()

                    # If new type are provided, clear the old ones and add the new ones
                    if new_type:
                        news.type.clear()
                        for type_id in new_type:
                            news.type.add(type_id)

                    # Delete old images and attachments only if new ones are provided
                    if new_images:
                        NewsImage.objects.filter(news=news).delete()
                    if new_attachments:
                        NewsAttachment.objects.filter(news=news).delete()

                    # Create new images and attachments if they are provided
                    for image in new_images:
                        NewsImage.objects.create(news=news, image=image)

                    for attachment in new_attachments:
                        NewsAttachment.objects.create(news=news, file=attachment)

                    return Response({"message": "更新成功"}, status=status.HTTP_200_OK)

                except Exception as e:
                    transaction.set_rollback(True)
                    return Response(
                        {"message": "更新失敗"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
        else:
            return Response(
                {"message": "錯誤的 id"}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request):
        news_id = request.query_params.get("id")
        if news_id is not None:
            try:
                news = News.objects.get(id=news_id)
                news.delete()
                response_data = {"message": "刪除成功"}
                return Response(response_data, status=status.HTTP_204_NO_CONTENT)
            except ObjectDoesNotExist:
                return Response(
                    {"message": "新聞不存在"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"message": "請提供有效的id"}, status=status.HTTP_400_BAD_REQUEST
            )


class NewsDownloadAPIView(APIView):
    def get(self, request):
        news_id = request.GET.get("id")
        try:
            news = News.objects.get(pk=news_id)
        except ObjectDoesNotExist:
            return Response(
                {"message": "此新聞不存在"}, status=status.HTTP_404_NOT_FOUND
            )

        attachments = news.newsAttachments.all()
        images = news.images.all()

        if not attachments and not images:
            return Response(
                {"message": "此新聞沒有附件也沒有圖片"}, status=status.HTTP_200_OK
            )

        zip_io = io.BytesIO()
        with zipfile.ZipFile(zip_io, "w", zipfile.ZIP_DEFLATED) as zipf:
            if attachments:
                for attachment in attachments:
                    # Add each file to the zip file
                    zipf.write(
                        attachment.file.path,
                        arcname=os.path.basename(attachment.file.name),
                    )

            if images:
                for image in images:
                    # Add each image to the zip file
                    zipf.write(
                        image.image.path, arcname=os.path.basename(image.image.name)
                    )

        # Reset file pointer to start
        zip_io.seek(0)

        now = datetime.now().strftime("%Y%m%d")  # Current time in the format 'YYYYMMDD'
        response = FileResponse(
            zip_io, as_attachment=True, filename="news_files_{}.zip".format(now)
        )

        return response


class AboutAPIView(APIView):
    def get(self, request):
        about_id = request.GET.get("id")
        if about_id is not None:
            try:
                about = About.objects.get(pk=about_id)
                serializer = AboutDetailSerializer(about, context={"request": request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response(
                    {"message": "此計畫內容不存在"}, status=status.HTTP_404_NOT_FOUND
                )

        abouts = About.objects.all().order_by("id")
        paginator = CustomPageNumberPagination()
        result_page = paginator.paginate_queryset(abouts, request)
        serializer = AboutSerializer(result_page, many=True)
        return Response(
            {
                "currentPage": paginator.page.number,
                "recordsPerPage": paginator.page_size,
                "totalPages": paginator.page.paginator.num_pages,
                "totalRecords": paginator.page.paginator.count,
                "records": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = AboutPostPatchSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "新增計畫介紹成功"}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        about_id = request.GET.get("id")
        if not about_id:
            return Response(
                {"message": "ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            about = About.objects.get(pk=about_id)
        except About.DoesNotExist:
            return Response(
                {"message": "此計畫內容不存在"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = AboutPostPatchSerializer(about, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "更新計畫介紹成功"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        about_id = request.GET.get("id")
        if not about_id:
            return Response(
                {"message": "ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            about = About.objects.get(pk=about_id)
            about.delete()
            return Response(
                {"message": "成功刪除計畫內容"}, status=status.HTTP_204_NO_CONTENT
            )
        except About.DoesNotExist:
            return Response(
                {"message": "此計畫內容不存在"}, status=status.HTTP_404_NOT_FOUND
            )


class AboutOutlineAPIView(APIView):
    def get(self, request):
        language = request.headers.get("Ltser-User-Language", "zh-tw")
        abouts = About.objects.all()
        serializer = AboutSerializer(abouts, many=True)
        response_data = {}
        project_introduction_data = []

        for data in serializer.data:
            name = data["name"] if language == "zh-tw" else data["name_en"]
            item_data = {"id": data["id"], "name": name}

            if data["type"] == "projectIntroduction":
                project_introduction_data.append(item_data)
            else:
                response_data.setdefault(data["type"], []).append(item_data)

        sorted_response_data = {"projectIntroduction": project_introduction_data}
        sorted_response_data.update(response_data)

        return Response(sorted_response_data)


class AboutAttachmentAPIView(APIView):
    def get(self, request):
        about_attachment_id = request.GET.get("id")
        if about_attachment_id is not None:
            try:
                about = AboutAttachment.objects.get(pk=about_attachment_id)
                serializer = AboutAttachmentSerializer(
                    about, context={"request": request}
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response(
                    {"message": "此計畫介紹補充資訊內容不存在"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        aboutAttachments = AboutAttachment.objects.all().order_by("id")
        paginator = CustomPageNumberPagination()
        result_page = paginator.paginate_queryset(aboutAttachments, request)
        serializer = AboutAttachmentSerializer(
            result_page, many=True, context={"request": request}
        )
        return Response(
            {
                "currentPage": paginator.page.number,
                "recordsPerPage": paginator.page_size,
                "totalPages": paginator.page.paginator.num_pages,
                "totalRecords": paginator.page.paginator.count,
                "records": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        image = request.FILES.get("image")
        file = request.FILES.get("file")
        if image:
            base, ext = os.path.splitext(image.name)
            if len(base) > 50:
                base = base[:50]
                image.name = f"{base}{ext}"
        if file:
            base, ext = os.path.splitext(file.name)
            if len(base) > 50:
                base = base[:50]
                file.name = f"{base}{ext}"

        serializer = AboutAttachmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "新增計畫介紹補充資訊成功"}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        about_attachment_id = request.GET.get("id")
        if not about_attachment_id:
            return Response(
                {"message": "ID is required for updating"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            about_attachment = AboutAttachment.objects.get(pk=about_attachment_id)
        except ObjectDoesNotExist:
            return Response(
                {"message": "Attachment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = AboutAttachmentSerializer(
            about_attachment, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "更新計畫介紹補充資訊成功"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        about_attachment_id = request.GET.get("id")
        if not about_attachment_id:
            return Response(
                {"message": "ID is required for deletion"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            about_attachment = AboutAttachment.objects.get(pk=about_attachment_id)
        except ObjectDoesNotExist:
            return Response(
                {"message": "Attachment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        about_attachment.delete()
        return Response(
            {"message": "刪除計畫介紹補充資訊成功"}, status=status.HTTP_200_OK
        )


class DownloadRecordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        paginator = CustomPageNumberPagination()
        records = DownloadRecord.objects.filter(user__id=user.id).order_by("-id")
        result_page = paginator.paginate_queryset(records, request)
        serializer = DownloadRecordSerializer(result_page, many=True)
        return Response(
            {
                "currentPage": paginator.page.number,
                "recordsPerPage": paginator.page_size,
                "totalPages": paginator.page.paginator.num_pages,
                "totalRecords": paginator.page.paginator.count,
                "records": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class DownloadApplyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({"message": "權限不足"}, status=status.HTTP_403_FORBIDDEN)

        user = request.user
        paginator = CustomPageNumberPagination()
        records = DownloadApply.objects.all().order_by("-id")
        result_page = paginator.paginate_queryset(records, request)
        serializer = DownloadApplySerializer(result_page, many=True)
        return Response(
            {
                "currentPage": paginator.page.number,
                "recordsPerPage": paginator.page_size,
                "totalPages": paginator.page.paginator.num_pages,
                "totalRecords": paginator.page.paginator.count,
                "records": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class SocialEconomyVisitorsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        visitor_id = request.query_params.get("id")
        if visitor_id is not None:
            visitor = SocialEconomyVisitors.objects.get(id=visitor_id)
            serializer = SocialEconomyVisitorsSerializer(visitor)
            return Response(serializer.data, status=status.HTTP_200_OK)

        visitor = SocialEconomyVisitors.objects.all().order_by("-year")

        paginator = CustomPageNumberPagination()
        result_page = paginator.paginate_queryset(visitor, request)
        serializer = SocialEconomyVisitorsSerializer(result_page, many=True)
        return Response(
            {
                "currentPage": paginator.page.number,
                "recordsPerPage": paginator.page_size,
                "totalPages": paginator.page.paginator.num_pages,
                "totalRecords": paginator.page.paginator.count,
                "records": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(request_body=SocialEconomyVisitorsSerializer)
    def post(self, request):
        serializer = SocialEconomyVisitorsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=SocialEconomyVisitorsSerializer)
    def patch(self, request):
        visitor_id = request.query_params.get("id")
        visitor = SocialEconomyVisitors.objects.get(id=visitor_id)
        serializer = SocialEconomyVisitorsSerializer(
            visitor, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        visitor_id = request.query_params.get("id")
        visitor = SocialEconomyVisitors.objects.get(id=visitor_id)
        visitor.delete()
        response_data = {"message": "刪除成功"}
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
