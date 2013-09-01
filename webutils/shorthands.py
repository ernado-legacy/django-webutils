import socket
import json as _json
from smtplib import SMTPException

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.mail import send_mail

mail = getattr(settings, 'FEEDBACK_MAIL', None)
password = getattr(settings, 'MAIL_PASSWORD', None)
server = getattr(settings, 'MAIL_SERVER', None)


class SendMailException(Exception):
    pass


def get_errors(form):
    return dict([(k, [unicode(e) for e in v]) for k, v in form.errors.items()])


def render(template, request, data=None, ):
    """
    Returns rendered template with provided context
    """
    return render_to_response(template, context_instance=RequestContext(request, data))


def json(data):
    """
    Returns the HttpResponse object with provided data in json
    """
    return HttpResponse(_json.dumps(data), mimetype='application/json')


def get_page(request, Model, count=10, query=None, prefix=None):
    """
    Returns the page
    """
    if not query:
        query = Model.objects.all()
    paginator = Paginator(query, count)
    page_number = request.GET.get('page', '1')

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    if prefix:
        key = 'page_%s%s' % (prefix, page.number)
        # TODO: Implement caching
    return page


def ensure(query):
    """
    Ensures that query has at least 1 element
    Raises Http404 if there is no elements in query
    """
    if len(query) < 1:
        raise Http404
    return query[0]


def format_price(price):
    """
    formats number 12345678 -> 12 345 678
    """
    s_list = []
    while price:
        s_list.append(str(price % 1000))
        price /= 1000
    s_list.reverse()
    return ' '.join(s_list).strip()


def send(subject, text, from_mail):
    """
    Sends email to FEEDBACK_MAIL e-mail address.
    """
    try:
        send_mail(subject, text, from_mail, mail, auth_user=server,
                  auth_password=password, fail_silently=False)
    except (SMTPException, socket.error) as e:
        raise SendMailException(e)


def send_generated(data):
    s, t, f = data
    send(s, t, f)