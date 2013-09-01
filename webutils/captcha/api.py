import urllib
from xml.etree.ElementTree import ElementTree

from django.conf import settings

key = getattr(settings, 'YANDEX_API_KEY')
api_url = 'http://cleanweb-api.yandex.ru/1.0/'
xml = ElementTree()


def check_spam(text):
    text = unicode(text).encode('utf-8')
    data = urllib.urlencode({'body-plain': text, 'key': key})
    print data
    f = urllib.urlopen(api_url + 'check-spam', data)
    print f
    xml.parse(f)
    return {'result': xml.find('text').get('spam-flag') == 'yes', 'id': xml.find('id').text}


def get_captcha(r_data=None):
    if not r_data:
        r_data = {'id': None}
    data = urllib.urlencode({'id': r_data['id'], 'key': key})
    f = urllib.urlopen(api_url + 'get-captcha', data)
    parsed_data = xml.parse(f)
    url = parsed_data.find('url').text
    captcha = parsed_data.find('captcha').text
    return {'url': url, 'captcha': captcha, 'id': r_data['id']}


def check_captcha(r_data):
    r_data.update({'key': key})
    data = urllib.urlencode(r_data)
    f = urllib.urlopen(api_url + 'check-captcha', data)
    return xml.parse(f).find('ok') is not None


def check_form(form, request):
    form_data = form.cleaned_data
    data = check_spam(form_data['message'])
    is_ok = True
    if request.POST.get('captcha_id'):
        check_data = {'value': request.POST.get('captcha_value'),
                      'captcha': request.POST.get('captcha_id'),
                      'id': request.POST.get('message_id')}
        is_ok = check_captcha(check_data)
    if data['result'] or not is_ok:
        captcha = get_captcha(data)
        return captcha
    return False


