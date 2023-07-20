How to trigger activity programaticaly in JS ?
----------------------------------------------

Call ``sessionSecurity.activity()`` [#script]_ every time you want to programaticaly trigger an activity.

.. [#script] http://django-session-security.readthedocs.org/en/master/_static/script.html#section-11

How to disable the "Are you sure you want to leave this page?" warning ?
------------------------------------------------------------------------

Include the JavaScript variable ``sessionSecurity.confirmFormDiscard = undefined;`` somewhere in your project *after* the plugin's JS. For example::

    <!-- base.html -->
    ...
    {% include 'session_security/all.html' %}
    <script>
        sessionSecurity.confirmFormDiscard = undefined;
    </script>
    ...
