from django.conf import settings
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash

from Member.models import Member


class MyAuthMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        super().process_request(request)
        if request.user is not None and request.user.id is not None:
            try:
                request.member = Member.objects.get(id=request.user.id)
            except:
                    request.member = request.user
        else:
            request.member = request.user
