# coding=utf-8
from django import forms
from django.core import validators
from widgets import YaCaptcha
from api import *
from django.utils.translation import ugettext_lazy as _


class YaCaptchaField(forms.CharField):
    default_error_messages = {
        'required': _(u'This field is required.'),
        'captcha_invalid': _(u'Пожалуйста, введите текст на картинке.')
    }

    def __init__(self, *args, **kwargs):
        self.required = True
        self.widget = YaCaptcha()  # код виджета ниже
        super(YaCaptchaField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return None
        return value

    def validate(self, values):
        super(YaCaptchaField, self).validate(values[0])
        recaptcha_challenge_value = values[0]  # пользовательский ввод
        recaptcha_response_value = values[1]   # код сессии от яндекса 
        check = check_captcha({'value': recaptcha_challenge_value, 'id': None, 'captcha': recaptcha_response_value})
        if not check:
            raise forms.ValidationError(self.error_messages['captcha_invalid'])