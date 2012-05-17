.. image:: https://secure.travis-ci.org/yourlabs/django-session-security.png?branch=master

This app provides a mechanism to logout inactive authenticated users. An
inactive browser should be logged out automatically if the user left his
workstation, to protect sensitive data that may be displayed in the browser. It
may be useful for CRMs, intranets, and such projects.

For example, if the user leaves for a coffee break, this app can force logout
after say 5 minutes of inactivity.

Requirements
------------

- Python 2.7
- jQuery 1.7+
- Django 1.4+
- django.contrib.staticfiles or django-staticfiles (included in Pinax) or
  you're on your own

Resources
---------

- `Git graciously hosted
  <https://github.com/yourlabs/django-session-security/>`_ by `GitHub
  <http://github.com>`_,
- `Documentation graciously hosted
  <http://django-session-security.rtfd.org>`_ by `RTFD
  <http://rtfd.org>`_,

.. Continuous integration graciously hosted by Travis:
.. http://travis-ci.org/yourlabs/django-session-security
.. Package graciously hosted by PyPi:
.. http://pypi.python.org/pypi/django-session-security/
