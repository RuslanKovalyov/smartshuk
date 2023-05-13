from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from user.models import CustomUser

# reCaptcha
from django import forms
from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV2Checkbox
from captcha.widgets import ReCaptchaV2Invisible
from django.conf import settings


class SignUpForm(UserCreationForm):
    if settings.ENABLE_RECAPTCHA:
        # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
        captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']
        if settings.ENABLE_RECAPTCHA:
            fields.append('captcha')


class LoginForm(AuthenticationForm):
    if settings.ENABLE_RECAPTCHA:
        # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
        captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        if settings.ENABLE_RECAPTCHA:
            fields.append('captcha')
