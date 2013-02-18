Quick setup
===========

The purpose of this documentation is to get you started as fast as possible,
because your time matters and you probably have other things to worry about.

Install the package::

    pip install django-session-security
    # or the development version
    pip install -e git+git://github.com/yourlabs/django-session-security.git#egg=django-session-security

For static file service, add to ``settings.INSTALLED_APPS``::

    'session_security',

Add to ``settings.MIDDLEWARE_CLASSES``, **after** django's AuthenticationMiddleware::

    'session_security.middleware.SessionSecurityMiddleware',

Ensure settings.TEMPLATE_CONTEXT_PROCESSORS has::

    'django.core.context_processors.request'

Add to urls::

    url(r'session_security/', include('session_security.urls')),

At this point, we're going to assume that you have `django.contrib.staticfiles
<https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/>`_ working.
This means that `static files are automatically served with runserver
<https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#runserver>`_,
and that you have to run `collectstatic when using another server
<https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#collectstatic>`_
(fastcgi, uwsgi, and whatnot). If you don't use django.contrib.staticfiles,
then you're on your own to manage staticfiles.

Add to your base template::

    {% include 'session_security/all.html' %}
