"""
One url meant to be used by JavaScript.

session_security_ping
    Connects the PingView.

To install this url, include it in ``urlpatterns`` definition in ``urls.py``,
ie::

    urlpatterns = patterns('',
        # ....
        url(r'session_security/', include('session_security.urls')),
        # ....
    )

"""
try:
    from django.conf.urls import url
except ImportError:
    from django.conf.urls.defaults import url

from .views import PingView

urlpatterns = [
    url(
        'ping/$',
        PingView.as_view(),
        name='session_security_ping',
    )
]
