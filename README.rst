.. image:: https://img.shields.io/pypi/v/django-session-security.svg
        :target: https://pypi.python.org/pypi/django-session-security

.. image:: https://img.shields.io/travis/yourlabs/django-session-security.svg
        :target: https://travis-ci.org/yourlabs/django-session-security


This app provides a mechanism to logout inactive authenticated users. An
inactive browser should be logged out automatically if the user left his
workstation, to protect sensitive data that may be displayed in the browser. It
may be useful for CRMs, intranets, and such projects.

For example, if the user leaves for a coffee break, this app can force logout
after say 5 minutes of inactivity.

Why not just set the session to expire after X minutes ?
--------------------------------------------------------

Or "Why does this app even exist" ? Here are the reasons:

- if the user session expires before the user is done reading a page: he will
  have to login again.
- if the user session expires before the user is done filling a form: his work
  will be lost, and he will have to login again, and probably yell at you, dear
  django dev ... at least I know I would !

This app allows to short circuit those limitations in session expiry.

How does it work ?
------------------

When the user loads a page, SessionSecurity middleware will set the last
activity to now. The last activity is stored as datetime
in ``request.session['_session_security']``. To avoid having the middleware
update that last activity datetime for a URL, add the url to
``settings.SESSION_SECURITY_PASSIVE_URLS``.

When the user moves mouse, click, scroll or press a key, SessionSecurity will
save the DateTime as a JavaScript attribute. It will send the number of seconds
since when the last user activity was recorded to PingView, next time it should
ping.

First, a warning should be shown after ``settings.SESSION_SECURITY_WARN_AFTER``
seconds. The warning displays a text like "Your session is about to expire,
move the mouse to extend it".

Before displaying this warning, SessionSecurity will upload the time since the
last client-side activity was recorded. The middleware will take it if it is
shorter than what it already has - ie. another more recent activity was
detected in another browser tab. The PingView will respond with the number of
seconds since the last activity - all browser tab included.

If there was no other, more recent, activity recorded by the server: it will
show the warning. Otherwise it will update the last activity in javascript from
the PingView response.

Same goes to expire after ``settings.SESSION_SECURITY_EXPIRE_AFTER`` seconds.
Javascript will first make an ajax request to PingView to ensure that another
more recent activity was not detected anywhere else - in any other browser tab.

Requirements
------------

- Python 2.7 or 3.5+
- jQuery 1.7+
- Django 1.8 to 2.0
- django.contrib.staticfiles or #YoYo

Resources
---------

You could subscribe to the mailing list ask questions or just be informed of
package updates.

- `Git graciously hosted
  <https://github.com/yourlabs/django-session-security/>`_ by `GitHub
  <http://github.com>`_,
- `Documentation graciously hosted
  <http://django-session-security.rtfd.org>`_ by `RTFD
  <http://rtfd.org>`_,
- `Package graciously hosted
  <http://pypi.python.org/pypi/django-session-security/>`_ by `PyPi
  <http://pypi.python.org/pypi>`_,
- `Mailing list graciously hosted
  <http://groups.google.com/group/yourlabs>`_ by `Google
  <http://groups.google.com>`_
- For **Security** issues, please contact yourlabs-security@googlegroups.com
- `Continuous integration graciously hosted
  <http://travis-ci.org/yourlabs/django-session-security>`_ by `Travis-ci
  <http://travis-ci.org>`_
