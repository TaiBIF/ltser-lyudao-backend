from django.contrib import admin
from .models import (
    MyUser,
    Contact,
    Literature,
    QATag,
    QuestionAnswer,
    FormLink,
    FormLinkAttachment,
    News,
    NewsTag,
    NewsImage,
    NewsAttachment,
    NewsCoverImage,
    About,
    AboutAttachment,
    DownloadRecord,
    DownloadApply,
)


class MyUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_email",
        "get_name",
        "get_groups",
        "get_verified",
        "get_last_login",
    )

    def get_email(self, obj):
        return obj.email

    def get_verified(self, obj):
        return obj.is_verified

    def get_name(self, obj):
        return obj.last_name + obj.first_name

    def get_last_login(self, obj):
        return obj.last_login

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    get_email.short_description = "EMAIL ADDRESS"
    get_verified.short_description = "VERIFIED STATUS"
    get_name.short_description = "NAME"
    get_last_login.short_description = "LAST LOGIN"
    get_groups.short_description = "GROUPS"


class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "name", "unit", "content", "contact")
    ordering = ["id"]


class LiteratureAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    ordering = ["id"]


class QATagAdmin(admin.ModelAdmin):
    list_display = ["title"]


class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ("type", "question", "answer")
    ordering = ["id"]


class FormLinkAttachmentInline(admin.StackedInline):
    model = FormLinkAttachment
    extra = 1


class FormLinkAdmin(admin.ModelAdmin):
    inlines = [FormLinkAttachmentInline]
    list_display = ("id", "name", "created_at", "updated_at", "has_attachments")

    def has_attachments(self, obj):
        return FormLinkAttachment.objects.filter(form_link=obj).exists()

    has_attachments.boolean = True
    has_attachments.short_description = "Attachments"


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1  # Number of extra "empty" forms


class NewsAttachmentInline(admin.TabularInline):
    model = NewsAttachment
    extra = 1


class NewsCoverImageInline(admin.StackedInline):
    model = NewsCoverImage
    can_delete = False
    verbose_name_plural = "News Cover Images"
    extra = 0
    max_num = 1


class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsCoverImageInline, NewsImageInline, NewsAttachmentInline]
    list_display = ["id", "title", "display_type", "newsDate", "display_content"]

    def display_type(self, obj):
        # 顯示多對多關聯字段 'type' 的名稱列表
        return ", ".join(tag.title for tag in obj.type.all())

    def display_content(self, obj):
        # 截取 'content' 字段的前 100 個字
        return obj.content[:100]

    display_type.short_description = "Type"  # 顯示的欄位名稱
    display_content.short_description = "Content"  # 顯示的欄位名稱


class NewsTagAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]


class AboutAttachmentInline(admin.TabularInline):
    model = AboutAttachment
    extra = 1


class AboutAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "name",
        "created_at",
        "updated_at",
    )  # 在列表中要顯示的字段
    list_filter = ("type",)  # 添加快速过滤选项
    search_fields = ("name", "content")  # 搜索框可以搜尋的字段
    inlines = [AboutAttachmentInline]  # 在 About 詳細頁面可以管理 AboutAttachment


class DownloadRecordAdmin(admin.ModelAdmin):
    list_display = ["id", "filename", "time", "user"]


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Literature, LiteratureAdmin)
admin.site.register(QATag, QATagAdmin)
admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
admin.site.register(FormLink, FormLinkAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(NewsTag, NewsTagAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(DownloadRecord, DownloadRecordAdmin)
