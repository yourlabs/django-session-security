from datetime import datetime, timedelta

from django.contrib import auth
from django.views import generic
from django import http

__all__ = ['PingView', ]


class PingView(generic.View):
    """
    View to update the last activity date time and get it.
    """

    def post(self, request, *args, **kwargs):
        """
        Return the **number of seconds since last activity**. Also, **update
        session's last activity if** ``sinceActivity`` GET argument is passed
        and superior to 0.

        - Use the ``sinceActivity`` and
          ``request.session['session_security']['last_activity']`` to calculate
          the last activity on the client (javascript), and on the server
          (django).

        - If the client reports a later last activity, then the session's last
          activity variable is updated according to the client.

        - Return the time since the last activity. Note that if the user
          generates activity in a browser tab, but not in the other, both will
          have the real last activity time because of this approach.

        To just query the actual last activity, let ``sinceActivity`` inferior
        to 0.
        """
        from settings import WARN_AFTER, EXPIRE_AFTER

        if 'session_security' not in request.session.keys():
            return http.HttpResponse('-1')

        now = datetime.now()
        last_activity = request.session['session_security']['last_activity']
        client_inactive_since = int(request.POST['inactiveSince'])
        server_inactive_since = (now - last_activity).seconds

        if client_inactive_since < server_inactive_since:
            # Client has more recent activity than we have in the session,
            # update the session.
            last_activity = (now
                - timedelta(seconds=client_inactive_since))

            # Update the session
            request.session['session_security']['last_activity'] = last_activity
            request.session.save()

        # We may now calculate how long the client has really been inactive
        inactive_for = (now - last_activity).seconds

        if inactive_for >= EXPIRE_AFTER:
            # It should have expired already.
            result = ('expire', -1)

            # Logout for consistency, even thought the middleware will do it at
            # next request on non-passive url.
            auth.logout(request)
        elif inactive_for >= WARN_AFTER:
            # Next step is expiry.
            result = ('expire', EXPIRE_AFTER - (now - last_activity).seconds)
        else:
            # Next step is the warning.
            result = ('warn', WARN_AFTER - (now - last_activity).seconds)

        return http.HttpResponse(u'["%s", %s]' % result)
