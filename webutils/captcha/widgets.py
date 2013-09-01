# coding=utf-8
from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from api import *

DEFAULT_WIDGET_TEMPLATE = 'captcha_widget.html'
WIDGET_TEMPLATE = DEFAULT_WIDGET_TEMPLATE


class YaCaptcha(forms.widgets.Widget):
    def __init__(self, key=None, *args, **kwargs):
        super(YaCaptcha, self).__init__(*args, **kwargs)

    # Вывод капчи
    def render(self, name, value, attrs=None):
        cap_dict = get_captcha()
        return render_to_string(WIDGET_TEMPLATE,
                                {'yacaptcha_img_url': cap_dict['url'],
                                 'yacaptcha_response_field': cap_dict['captcha']  # Проверочный код сессии яндекса
                                })

    # Выборка данных из словаря значений формы
    def value_from_datadict(self, data, files, name):
        return [data.get('captcha', None), data.get('yacaptcha_response_field', None)]