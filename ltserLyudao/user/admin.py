from django.contrib import admin
from .models import MyUser, Contact, Literature, QATag, QuestionAnswer, FormLink, FormLinkAttachment, News, NewsTag, \
    NewsImage, NewsAttachment
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_email', 'get_name', 'get_verified', 'get_last_login')

    def get_email(self, obj):
        return obj.email

    def get_verified(self, obj):
        return obj.is_verified

    def get_name(self, obj):
        return obj.last_name + obj.first_name

    def get_last_login(self, obj):
        return obj.last_login

    get_email.short_description = 'EMAIL ADDRESS'
    get_verified.short_description = 'VERIFIED STATUS'
    get_name.short_description = 'NAME'
    get_last_login.short_description = 'LAST LOGIN'

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'name', 'unit', 'content', 'contact')
    ordering = ['id']

class LiteratureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ['id']


class QATagAdmin(admin.ModelAdmin):
    list_display = ['title']

class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('type', 'question', 'answer')
    ordering = ['id']

class FormLinkAttachmentInline(admin.StackedInline):
    model = FormLinkAttachment
    extra = 1

class FormLinkAdmin(admin.ModelAdmin):
    inlines = [FormLinkAttachmentInline]
    list_display = ('id', 'name', 'created_at', 'updated_at', 'has_attachments')

    def has_attachments(self, obj):
        return FormLinkAttachment.objects.filter(form_link=obj).exists()
    has_attachments.boolean = True
    has_attachments.short_description = 'Attachments'

class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1  # Number of extra "empty" forms

class NewsAttachmentInline(admin.TabularInline):
    model = NewsAttachment
    extra = 1

class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsImageInline, NewsAttachmentInline]
    list_display = ['id', 'title', 'user', 'newsDate', 'count_images', 'count_attachments']

    def count_images(self, obj):
        return obj.images.count()

    count_images.short_description = 'Images Count'

    def count_attachments(self, obj):
        return obj.newsAttachments.count()

    count_attachments.short_description = 'Attachments Count'

class NewsTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Literature, LiteratureAdmin)
admin.site.register(QATag, QATagAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
admin.site.register(FormLink, FormLinkAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(NewsTag, NewsTagAdmin)