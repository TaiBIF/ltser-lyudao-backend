from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.exceptions import ValidationError
class CustomPasswordValidator(MinimumLengthValidator):
    def validate(self, password, user=None):
        super().validate(password, user)
        if len(password) < 8:
            raise ValidationError("密码必须至少包含8个字符。")
        if not any(char.isdigit() for char in password):
            raise ValidationError("密码必须包含至少一个数字。")
        if not any(char.isalpha() for char in password):
            raise ValidationError("密码必须包含至少一个英文字母。")
