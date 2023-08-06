#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

import re
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.static import serve
from django.contrib.staticfiles.views import serve as serve_static
from django.shortcuts import redirect, render
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import ImproperlyConfigured

from .namegen.namegen import NameGenerator

from .utils import setting

User = get_user_model()

DJANGO_QUICKY_SUPERUSER_USERNAME = getattr(
    settings,
    'DJANGO_QUICKY_SUPERUSER_USERNAME',
    'admin'
)

DJANGO_QUICKY_SUPERUSER_PASSWORD = getattr(
    settings,
    'DJANGO_QUICKY_SUPERUSER_PASSWORD',
    'admin'
)

DJANGO_QUICKY_SUPERUSER_EMAIL = getattr(
    settings,
    'DJANGO_QUICKY_SUPERUSER_EMAIL',
    'admin@admin.admin'
)

DJANGO_QUICKY_AUTOLOGIN = getattr(
    settings,
    'DJANGO_QUICKY_AUTOLOGIN',
    None
)

def force_super_user_middleware(get_response):

    class_middleware = ForceSuperUserMiddleWare()

    def middleware(request):
        class_middleware.process_request(request)
        response = get_response(request)
        return response

    return middleware


class ForceSuperUserMiddleWare(MiddlewareMixin):
    """
        Developpement middleware forcing login with a super user so you
        don't have to login or worry about access rights.
    """

    def process_request(self, request):

        try:
            request.user = User.objects.filter(is_superuser=True)[0]
        except (User.DoesNotExist, IndexError):
            request.user = User.objects.create_superuser(
                username=DJANGO_QUICKY_SUPERUSER_USERNAME,
                email=DJANGO_QUICKY_SUPERUSER_PASSWORD,
                password=DJANGO_QUICKY_SUPERUSER_EMAIL
            )

class AutoLoginMiddleWare(MiddlewareMixin):
    """
        Developpement middleware forcing login with a given user so you
        don't have to login.
    """

    def process_request(self, request):

        if DJANGO_QUICKY_AUTOLOGIN is None:
            raise ImproperlyConfigured(
                "You muse set DJANGO_QUICKY_AUTOLOGIN to an existing username "
                "if you want to use AutoLoginMiddleWare."
            )
        try:
            request.user = User.objects.filter(username=DJANGO_QUICKY_AUTOLOGIN)[0]
        except (User.DoesNotExist, IndexError):
            raise ImproperlyConfigured((
                "The AutoLoginMiddleWare can't find the user '{}' in database. "
                "Check the value of DJANGO_QUICKY_AUTOLOGIN and the User table."
            ).format(DJANGO_QUICKY_AUTOLOGIN))


class StaticServe(object):
    """
        Django middleware for serving static files instead of using urls.py.

        It serves them wether you are set DEBUG or not, so put it into
        a separate settings file to activate it at will.
    """

    # STATIC_URL must be defined at least
    static_url = settings.STATIC_URL.rstrip('/')

    # try to get MEDIA_URL
    media_url = setting('MEDIA_URL', '').rstrip('/')

    # try to get MEDIA_URL
    admin_url = setting('ADMIN_MEDIA_PREFIX', '').rstrip('/')

    media_regex = re.compile(r'^%s/(?P<path>.*)$' % media_url)
    static_regex = re.compile(r'^%s/(?P<path>.*)$' % static_url)
    admin_regex = re.compile(r'^%s/(?P<path>.*)$' % admin_url)

    # IF not MEDIA_ROOT is defined, we supposed it's the same as the
    # STATIC_ROOT
    MEDIA_ROOT = setting('MEDIA_ROOT') or setting('STATIC_ROOT')
    ADMIN_ROOT = setting('ADMIN_MEDIA_PREFIX') or setting('STATIC_ROOT')


    def process_request(self, request):

        protocol = 'http' + ('', 's')[request.is_secure()]
        host = request.META.get('HTTP_HOST', setting(
            'DJANGO_QUICKY_DEFAULT_HOST', 'django_quicky_fake_host'))
        prefix = protocol + '://' + host
        abspath = prefix + request.path

        if self.media_url:
            path = abspath if prefix in self.media_url else request.path
            match = self.media_regex.search(path)
            if match:
                return serve(request, match.group(1), self.MEDIA_ROOT)

        if self.admin_url:
            path = abspath if prefix in self.admin_url else request.path
            match = self.admin_regex.search(path)
            if match:
                return serve(request, match.group(1), self.ADMIN_ROOT)

        path = abspath if prefix in self.static_url else request.path
        match = self.static_regex.search(path)
        if match:
            return serve_static(request, match.group(1), insecure=True)


class AutoLogNewUser(object):


    CALLBACK = setting('AUTOLOGNEWUSER_CALLBAK', None)


    def process_request(self, request):


        if 'django-quicky-test-cookie' in request.path:

            if not request.session.test_cookie_worked():
                return render(request, 'django_quicky/no_cookies.html',
                              {'next': request.GET.get('next', '/')})

            request.session.delete_test_cookie()

            first_name = iter(NameGenerator()).next().title()
            username = "%s%s" % (first_name, random.randint(10, 100))
            user = User.objects.create(username=username,
                                       first_name=first_name)
            request.session['django-quicky:user_id'] = user.pk
            next = request.GET.get('next', '/')
            if self.CALLBACK:
                res = self.CALLBACK(request)
            return redirect(res or next)

        if not request.user.is_authenticated():

            user_id = request.session.get('django-quicky:user_id', None)

            if not user_id:

                request.session.set_test_cookie()
                return redirect('/django-quicky-test-cookie/?next=%s' % request.path)

            request.user = User.objects.get(pk=user_id)


