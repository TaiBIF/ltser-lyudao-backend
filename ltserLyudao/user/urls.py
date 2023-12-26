from django.urls import path
from .views import ContactAPIView, LiteratureAPIView, RegisterAPIView, QATagAPIView, QuestionAnswerAPIView, \
    FormLinkAPIVIew, FormLinkDownloadAPIview, NewsTagAPIView, NewsAPIView, VerifyEmailAPIView, \
    ResendEmailVerifyAPIView, LoginAPIView, UpdateUserPasswordAPIView, RequestPasswordResetEmailAPIView, \
    PasswordTokenCheckAPIView, SetNewPasswordAPIView, UserIdentityAPIView, AboutAPIView, AboutOutlineAPIView, \
    AboutAttachmentAPIView, ContactAllAPIView, DownloadRecordAPIView, DownloadApplyAPIView, GoogleAuthAPIView, MemberInformationAPIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/google/', GoogleAuthAPIView.as_view(), name='google-auth'),
    path('auth/signUp/', RegisterAPIView.as_view(), name='signUp'),
    path('auth/email-verify/', VerifyEmailAPIView.as_view(), name='email-verify'),
    path('auth/resend-email-verify/', ResendEmailVerifyAPIView.as_view(), name='resend-email-verify'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/updateUserPassword/', UpdateUserPasswordAPIView.as_view(), name='update-user-password'),
    path('auth/request-rest-email/', RequestPasswordResetEmailAPIView.as_view(), name='request-rest-email'),
    path('auth/password-reset/<uidb64>/<token>/', PasswordTokenCheckAPIView.as_view(), name='password-reset-confirm'),
    path('auth/password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    path('auth/identity/', UserIdentityAPIView.as_view(), name='identity'),
    path('users/contacts/', ContactAPIView.as_view(), name='contact'),
    path('users/contacts-all/', ContactAllAPIView.as_view(), name='contact-all'),
    path('users/literatures/', LiteratureAPIView.as_view(), name='literature'),
    path('users/qatags/', QATagAPIView.as_view(), name='qatag'),
    path('users/question-answers/', QuestionAnswerAPIView.as_view(), name='question-answers'),
    path('users/form-link/', FormLinkAPIVIew.as_view(), name='form-link'),
    path('download/form-link/', FormLinkDownloadAPIview.as_view(), name='form-link-attachments-download'),
    path('users/newstags/', NewsTagAPIView.as_view(), name='newsTag'),
    path('users/news/', NewsAPIView.as_view(), name='news'),
    path('users/about/', AboutAPIView.as_view(), name='about'),
    path('users/about-outline/', AboutOutlineAPIView.as_view(), name='about-outline'),
    path('users/about-attachment/', AboutAttachmentAPIView.as_view(), name='about-attachment'),
    path('users/download-record/', DownloadRecordAPIView.as_view(), name='download-record'),
    path('users/download-apply/', DownloadApplyAPIView.as_view(), name='download-apply'),
    path('users/member-info/', MemberInformationAPIView.as_view(), name='member-info'),
]
