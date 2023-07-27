from rest_framework import serializers
from .models import Contact, Literature, MyUser, QATag, QuestionAnswer, FormLink, FormLinkAttachment, NewsTag, News, \
    NewsImage, NewsAttachment, NewsCoverImage
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import RegexValidator

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=MyUser.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True,
                                     validators=[RegexValidator(regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d\!\@\#\$\%\^\&\*\(\)\-\_\+\=\{\}\[\]\:\;\.\,]{8,}$'
,message="密碼長度至少8位，並且包含至少一個英文字母和一個數字")])
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)


    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = MyUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=255, min_length=8, write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ['email', 'password', 'token']

    @staticmethod
    def get_token(obj):
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'type', 'name', 'unit', 'content', 'contact', 'image']

    def create(self, validated_data):
        contact = Contact.objects.create(**validated_data)
        return contact


class LiteratureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Literature
        fields = ['id', 'name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        return Literature.objects.create(**validated_data)

class QATagSerializer(serializers.ModelSerializer):
    class Meta:
        model = QATag
        fields = ['id', 'title', 'created_at', 'updated_at']

class QuestionAnswerSerializer(serializers.ModelSerializer):
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=QATag.objects.all(),
        source='type',
    )

    class Meta:
        model = QuestionAnswer
        fields = ['id', 'type_id', 'question', 'answer', 'created_at', 'updated_at']

    def create(self, validated_data):
        type_instance = validated_data.pop('type')
        validated_data['type'] = type_instance
        return super().create(validated_data)

    def update(self, instance, validated_data):
        type_instance = validated_data.pop('type')
        validated_data['type'] = type_instance
        return super().update(instance, validated_data)

class FormLinkAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormLinkAttachment
        fields = ['file']

class FormLinkSerializer(serializers.ModelSerializer):
    attachments = FormLinkAttachmentSerializer(many=True, read_only=True, source='formLinkAttachments')

    class Meta:
        model = FormLink
        fields = ('id', 'name', 'created_at', 'link', 'attachments')

class NewsTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTag
        fields = ['id', 'title', 'created_at', 'updated_at']

class NewsSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    class Meta:
        model = News
        fields = ['id', 'type', 'title', 'content', 'newsDate']

    def get_content(self, obj):
        # 獲取 content 字段的前 100 個字
        return obj.content[:100]

class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ['image']


class NewsAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsAttachment
        fields = ['file']

class NewsCoverImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCoverImage
        fields = ['image']

class NewsDetailSerializer(serializers.ModelSerializer):
    images = NewsImageSerializer(many=True, read_only=True)
    attachments = NewsAttachmentSerializer(many=True, read_only=True, source='newsAttachments')
    user_email = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()  # Add this line

    class Meta:
        model = News
        fields = ['id', 'type', 'title', 'content', 'newsDate', 'user', 'user_email', 'images', 'attachments', 'cover']

    def get_user_email(self, obj):
        # 獲取 user 的 email
        return obj.user.email

    def get_cover(self, obj):  # Add this method
        if obj.cover_image:
            return obj.cover_image.image.url
        return None