"""
Two urls meant to be used by javascript.

session_security_ping
    Checks the server side status of the session.
"""

from django.conf.urls.defaults import url, patterns
from django.contrib.auth.decorators import login_required

from views import PingView

urlpatterns = patterns('',
    url(
        'ping/$',
        PingView.as_view(),
        name='session_security_ping',
    ),
)
