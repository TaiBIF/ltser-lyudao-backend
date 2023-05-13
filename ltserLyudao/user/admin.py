from django.contrib import admin
from .models import MyUser
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('get_email', 'get_name', 'get_verified', 'get_last_login')

    def get_email(self, obj):
        return obj.email

    def get_verified(self, obj):
        return obj.is_verified

    def get_name(self, obj):
        return obj.first_name+obj.last_name

    def get_last_login(self, obj):
        return obj.last_login

    get_email.short_description = 'EMAIL ADDRESS'
    get_verified.short_description = 'VERIFIED STATUS'
    get_name.short_description = 'NAME'
    get_last_login.short_description = 'LAST LOGIN'

admin.site.register(MyUser, MyUserAdmin)