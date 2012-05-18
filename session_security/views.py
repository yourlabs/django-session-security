import datetime

from django.contrib import auth
from django.views import generic
from django import http

__all__ = ['PingView', ]


class PingView(generic.View):
    """
    Return the number of seconds since last activity. Also, update session's
    last activity if sinceActivity GET argument is passed and > 0.

    The first thing this view does, is use the sinceActivity request paramater
    and session last_activity to calculate the last activity on the client, and
    on the server.

    If the client reports a later last activity, then the session's last
    activity variable is updated according to the client.

    Return the time since the last activity. Note that if the user generates
    activity in a browser tab, but not in the other, both will have the real
    last activity time because of this approach.

    If the client just wants to poll for the time since the real last activity,
    then it should pass a sinceActivity inferior to 0.
    """

    def get(self, request, *args, **kwargs):
        from settings import WARN_AFTER, EXPIRE_AFTER

        now = datetime.datetime.now()

        if 'session_security' not in request.session.keys():
            return http.HttpResponse('-1')
        data = request.session['session_security']

        client_since_activity = int(request.GET['sinceActivity'])
        client_last_activity = now - datetime.timedelta(
            seconds=client_since_activity)

        server_last_activity = data['last_activity']
        server_since_activity = (now - server_last_activity).seconds

        if client_since_activity < 0 or \
            server_last_activity > client_last_activity:

            last_activity = server_last_activity
            since_activity = server_since_activity
        else:
            last_activity = client_last_activity
            since_activity = client_since_activity

            data['last_activity'] = client_last_activity
            request.session['session_security'] = data
            request.session.save()

        if since_activity > EXPIRE_AFTER:
            auth.logout(request)

        return http.HttpResponse(since_activity)
