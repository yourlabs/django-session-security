"""
SessionSecurityMiddleware is the heart of the security that this application
attemps to provide.

To install this middleware, add to your ``settings.MIDDLEWARE_CLASSES``::

    'session_security.middleware.SessionSecurityMiddleware'

Make sure that it is placed **after** authentication middlewares
and message middleware.
"""

from datetime import datetime, timedelta

from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.utils.translation import ugettext as _

from .utils import get_last_activity, set_last_activity
from .settings import (EXPIRE_AFTER, PASSIVE_URLS,
                       SHOW_MESSAGE_AFTER_AUTO_LOGOUT)


class SessionSecurityMiddleware(object):
    """
    In charge of maintaining the real 'last activity' time, and log out the
    user if appropriate.
    """

    def process_request(self, request):
        """ Update last activity time or logout. """
        if not request.user.is_authenticated():
            return

        now = datetime.now()
        self.update_last_activity(request, now)

        delta = now - get_last_activity(request.session)
        if delta.seconds >= EXPIRE_AFTER:
            if SHOW_MESSAGE_AFTER_AUTO_LOGOUT:
                messages.info(request, _('You have been disconnected '
                                         'because it became too long '
                                         'without activity.'))
            logout(request)
        elif request.path not in PASSIVE_URLS:
            set_last_activity(request.session, now)

    def update_last_activity(self, request, now):
        """
        If ``request.GET['idleFor']`` is set, check if it refers to a more
        recent activity than ``request.session['_session_security']`` and
        update it in this case.
        """
        if '_session_security' not in request.session:
            set_last_activity(request.session, now)

        last_activity = get_last_activity(request.session)
        server_idle_for = (now - last_activity).seconds

        if (request.path == reverse('session_security_ping') and
                'idleFor' in request.GET):
            # Gracefully ignore non-integer values
            try:
                client_idle_for = int(request.GET['idleFor'])
            except ValueError:
                return

            # Disallow negative values, causes problems with delta calculation
            if client_idle_for < 0:
                client_idle_for = 0

            if client_idle_for < server_idle_for:
                # Client has more recent activity than we have in the session
                last_activity = now - timedelta(seconds=client_idle_for)

                # Update the session
                set_last_activity(request.session, last_activity)
