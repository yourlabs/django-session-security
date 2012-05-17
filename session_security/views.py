import datetime

from django.views import generic
from django import http

from settings import EXPIRE_AFTER, WARN_BEFORE

class ExtendSessionView(generic.View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return http.HttpResponseForbidden()

        now = datetime.datetime.now()
        request.session['session_security']['last_activity'] = now
        return http.HttpResponse()
