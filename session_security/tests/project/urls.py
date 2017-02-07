import time

from django.conf.urls import include, url

try:
    from django.conf.urls import patterns
except ImportError:
    patterns = None

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.decorators import login_required
from django.views import generic


class SleepView(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        time.sleep(int(request.GET.get('seconds', 0)))
        return super(SleepView, self).get(request, *args, **kwargs)


urlpatterns = [
    url(r'^$', generic.TemplateView.as_view(template_name='home.html')),
    url(r'^sleep/$', login_required(
        SleepView.as_view(template_name='home.html')), name='sleep'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'session_security/', include('session_security.urls')),
    url(r'^ignore/$', login_required(
        generic.TemplateView.as_view(template_name='home.html')), name='ignore'),
]

if patterns:
    urlpatterns = patterns('', *urlpatterns)
