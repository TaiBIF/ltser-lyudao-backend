from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

class MyUserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        if username is None:
            raise TypeError('創建使用者必須輸入 username')
        if email is None:
            raise TypeError('創建使用者必須輸入 email')

        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('創建管理員必須輸入 password')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_verified = True
        user.is_staff = True
        user.save()
        return user

class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_regular_user = models.BooleanField(default=True, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_social_project_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])


class Contact(models.Model):
    TYPE_CHOICES = [
        ('leader', '計畫總主持人'),
        ('executor', '計畫執行人員'),
        ('other', '其他人員'),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    name = models.CharField(max_length=255, blank=False, null=False)
    name_en = models.CharField(max_length=255, blank=False, null=True)
    unit = models.CharField(max_length=255, blank=False, null=False)
    unit_en = models.CharField(max_length=255, blank=False, null=True)
    content = models.CharField(max_length=255, blank=False, null=False)
    content_en = models.CharField(max_length=255, blank=False, null=True)
    contact = models.CharField(max_length=255, blank=False, null=False)
    image = models.ImageField(upload_to='images', blank=False, null=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    class Meta:
        db_table = 'Contact'


class Literature(models.Model):
    name = models.CharField(max_length=500, blank=False, null=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    year = models.IntegerField(null=True, blank=False)

    class Meta:
        db_table = 'Literature'


class QATag(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    title_en = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    def __str__(self):
        return f"{self.title}"
    class Meta:
        db_table = 'QATag'

class QuestionAnswer(models.Model):
    type = models.ForeignKey(QATag, on_delete=models.CASCADE)
    question = models.CharField(max_length=1000, blank=False, null=False)
    question_en = models.CharField(max_length=1000, blank=True, null=True)
    answer = models.TextField()
    answer_en = models.TextField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'QuestionAnswer'

class FormLink(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField(null=True, blank=True, default="")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'FormLink'

class FormLinkAttachment(models.Model):
    form_link = models.ForeignKey(FormLink, on_delete=models.CASCADE, related_name='formLinkAttachments')
    file = models.FileField(upload_to='formLinkAttachments')

    class Meta:
        db_table = 'FormLinkAttachment'


class NewsTag(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    def __str__(self):
        return f"{self.title}"
    class Meta:
        db_table = 'NewsTag'

class News(models.Model):
    type = models.ManyToManyField('NewsTag', blank=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    newsDate = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    cover_image = models.OneToOneField('NewsCoverImage', null=True, blank=True, on_delete=models.SET_NULL,
                                       related_name='news_cover_image')
    class Meta:
        db_table = 'News'


class NewsCoverImage(models.Model):
    news = models.OneToOneField(News, related_name='newsCoverImage', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='newsCoverImages')

    def __str__(self):
        return f"{self.image}"
    class Meta:
        db_table = 'NewsCoverImage'


class NewsImage(models.Model):
    news = models.ForeignKey(News, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='newsImages', blank=True, null=True)

    def __str__(self):
        return f"{self.image}"

    class Meta:
        db_table = 'NewsImage'

class NewsAttachment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='newsAttachments')
    file = models.FileField(upload_to='newsAttachments')

    class Meta:
        db_table = 'NewsAttachment'

class About(models.Model):
    TYPE_CHOICES = [
        ('ecologicalObservation', '生態觀測'),
        ('environmentalObservation', '環境觀測'),
        ('socialObservation', '社會觀測'),
        ('projectIntroduction', '計畫介紹')
    ]

    type = models.CharField(max_length=200, choices=TYPE_CHOICES)
    name = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField()
    content_en = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="aboutImage", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
    class Meta:
        db_table = 'About'


class AboutAttachment(models.Model):
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name='aboutAttachments')
    name = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    content_en = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='aboutAttachments', null=True, blank=True)
    image = models.ImageField(upload_to='aboutAttachments', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'AboutAttachment'

    def __str__(self):
        return f"{self.name}"

class DownloadRecord(models.Model):
    filename = models.CharField(max_length=200)
    time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='download_records')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.filename}"
    class Meta:
        db_table = 'DownloadRecord'

class DownloadApply(models.Model):
    email = models.EmailField(max_length=255)
    role = models.CharField(max_length=255)
    content = models.TextField()
    filename = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.email}"
    class Meta:
        db_table = 'DownloadApply'

class SocialEconomyVisitors(models.Model):
    year = models.IntegerField(null=True, blank=False)
    visitors = models.IntegerField(null=False, blank=False)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'SocialEconomyVisitors'

