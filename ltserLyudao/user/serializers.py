from rest_framework import serializers
from .models import Contact, Literature, MyUser, QATag, QuestionAnswer, FormLink, FormLinkAttachment, NewsTag, News, \
    NewsImage, NewsAttachment
from django.utils.translation import gettext
from rest_framework.validators import UniqueValidator
from drf_yasg.openapi import Schema, TYPE_STRING
from drf_yasg.utils import swagger_serializer_method
from drf_yasg import openapi

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=MyUser.objects.all())]
    )
    password = serializers.CharField(
        max_length=68,
        min_length=8,
        write_only=True,
        error_messages={
            'min_length': gettext('密碼至少8位數'),
            'required': gettext('密碼是必填'),
        }
    )
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True, error_messages={
        'required': gettext('需要填入名')
    })
    last_name = serializers.CharField(required=True, error_messages={
        'required': gettext('需要填入姓')
    })
    class Meta:
        model = MyUser
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')

    @staticmethod
    def validate_password(value):
        # 自定义验证逻辑
        has_letter = False
        has_number = False

        for char in value:
            if char.isalpha():
                has_letter = True
            elif char.isdigit():
                has_number = True

        if not (has_letter and has_number):
            raise serializers.ValidationError(gettext('密碼必須包含至少一個字母和一個數字'))

        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"message": "密碼欄位不相符"})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return MyUser.objects.create_user(**validated_data)

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


class NewsDetailSerializer(serializers.ModelSerializer):
    images = NewsImageSerializer(many=True, read_only=True)
    attachments = NewsAttachmentSerializer(many=True, read_only=True, source='newsAttachments')
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'type', 'title', 'content', 'newsDate', 'user', 'user_email', 'images', 'attachments']

    def get_user_email(self, obj):
        # 獲取 user 的 email
        return obj.user.email