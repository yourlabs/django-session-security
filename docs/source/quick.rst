Quick setup
===========

The purpose of this documentation is to get you started as fast as possible,
because your time matters and you probably have other things to worry about.

Install the package::

    pip install django-session-security

For static file service, add ``session_security`` to your ``INSTALLED_APPS`` settings:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'session_security',
        # ...
    ]

Add ``session_security.middleware.SessionSecurityMiddleware`` to your ``MIDDLEWARE`` settings:

.. code-block:: python

    MIDDLEWARE = [
        # ...
        'session_security.middleware.SessionSecurityMiddleware',
        # ...
    ]

.. warning::

    The order of ``MIDDLEWARE`` is important. You should include the ``django-session-security`` middleware
    after the authentication middleware, such as :class:`~django.contrib.auth.middleware.AuthenticationMiddleware`.

Ensure ``django.template.context_processors.request`` is added to the template context processors:

.. code-block:: python

    TEMPLATES = [
        {
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.request",
                    # ...
                ]
            }
            # ...
        }
    ]

Add ``session_security`` URLs to your project’s URLconf:

.. code-block:: python

    from django.urls import include, path

    urlpatterns = [
        # ...
        path('session_security/', include('session_security.urls')),
    ]

At this point, we're going to assume that you have `django.contrib.staticfiles
<https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/>`_ working.
This means that `static files are automatically served with runserver
<https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#runserver>`_,
and that you have to run `collectstatic when using another server
<https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#collectstatic>`_
(fastcgi, uwsgi, and whatnot). If you don't use `django.contrib.staticfiles`,
then you're on your own to manage staticfiles.

After jQuery, add to your base template::

    {% include 'session_security/all.html' %}
