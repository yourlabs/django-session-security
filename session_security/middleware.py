import datetime

from django import http
from django.contrib.auth import logout

from settings import LOGOUT_URL, LOGIN_URL, EXPIRE_AFTER, WARN_BEFORE

class SessionSecurityMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            return

        now = datetime.datetime.now()
        data = request.session.get('session_security', {
            'LOGOUT_URL': LOGOUT_URL,
            'LOGIN_URL': LOGIN_URL,
            'EXPIRE_AFTER': EXPIRE_AFTER,
            'WARN_BEFORE': WARN_BEFORE,
            'last_activity': now,
        })

        delta = now - data['last_activity']
        if delta.seconds > EXPIRE_AFTER and request.path_info != LOGIN_URL:
            logout(request)
            return http.HttpResponseRedirect(
                '%s?next=%s' % (LOGIN_URL, request.path_info))
   
        data['last_activity'] = now
        request.session['session_security'] = data
