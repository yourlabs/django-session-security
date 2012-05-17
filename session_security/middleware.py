import datetime

from django import http
from django.contrib.auth import logout

from settings import LOGIN_URL, SECONDS

class SessionSecurityMiddleware(object):
    def process_request(self, request):
        now = datetime.datetime.now()
        last_activity = request.session.get('last_activity', now)
        delta = now - last_activity
        
        if delta.seconds > SECONDS and request.path_info != LOGIN_URL:
            logout(request)
            return http.HttpResponseRedirect(
                '%s?next=%s' % (LOGIN_URL, request.path_info))
   
        request.session['last_activity'] = now
        # javascript should have a margin of 10 for page rendering
        request.session['session_expiry_seconds'] = SECONDS - 10

