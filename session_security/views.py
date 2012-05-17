import datetime

from django.views import generic
from django import http

from settings import EXPIRE_AFTER, WARN_BEFORE

class PingView(generic.View):
     def post(self, request, *args, **kwargs):
        now = datetime.datetime.now()

        if 'session_security' not in request.session.keys():
            return http.HttpResponse('expire')

        last = request.session['session_security']['last_activity']
        delta = now - last

        if delta.seconds > EXPIRE_AFTER:
            return http.HttpResponse('expire')
        elif delta.seconds > EXPIRE_AFTER - WARN_BEFORE:
            return http.HttpResponse('warn')
        else:
            return http.HttpResponse(delta.seconds)

class ExtendSessionView(generic.View):
    def post(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        request.session['session_security']['last_activity'] = now
        return http.HttpResponse()
