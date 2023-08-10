from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver
from .models import MyUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

@receiver(social_account_added)
def create_myuser(sender, request, sociallogin, **kwargs):
    # 從 sociallogin 獲取用戶資訊
    user_data = {
        'email': sociallogin.user.email,
        'username': sociallogin.user.name,
        'first_name': sociallogin.user.given_name,
        'last_name': sociallogin.user.family_name,
    }

    # 根據 email 尋找或建立 MyUser 實例
    myuser, created = MyUser.objects.update_or_create(
        email=user_data['email'],
        defaults=user_data
    )

    if created:
        # 做一些初始設定，如分配角色、建立相關資料等

        # 例如：更新上次登入時間
        myuser.update_last_login()


