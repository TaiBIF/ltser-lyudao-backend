from django.contrib import admin
from .models import MyUser, Contact
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
    
admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Contact, ContactAdmin)