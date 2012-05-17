from django.conf.urls.defaults import url, patterns

from views import ExtendSessionView

urlpatterns = patterns('',
    url(
        'extend/$',
        ExtendSessionView.as_view(),
        name='session_security_extend_session',
    ),
)
