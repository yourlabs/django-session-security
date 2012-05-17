"""
Two urls meant to be used by javascript.

session_security_ping
    Checks the server side status of the session.

session_security_extend_session
    Artificially update last_activity to postpone session expiry.
"""

from django.conf.urls.defaults import url, patterns
from django.contrib.auth.decorators import login_required

from views import ExtendSessionView, PingView

urlpatterns = patterns('',
    url(
        'ping/$',
        PingView.as_view(),
        name='session_security_ping',
    ),
    url(
        'extend/$',
        login_required(ExtendSessionView.as_view()),
        name='session_security_extend_session',
    ),
)
