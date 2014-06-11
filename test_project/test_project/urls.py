import time

from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.decorators import login_required
from django.views import generic


class SleepView(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        time.sleep(int(request.GET.get('seconds', 0)))
        return super(SleepView, self).get(request, *args, **kwargs)

urlpatterns = patterns('',
    url(r'^favicon\.ico$', generic.RedirectView.as_view(
        url=settings.STATIC_URL + '/favicon.ico')),
    url(r'^$', generic.TemplateView.as_view(template_name='home.html')),
    url(r'^sleep/$', login_required(
        SleepView.as_view(template_name='home.html')), name='sleep'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'session_security/', include('session_security.urls')),
)
