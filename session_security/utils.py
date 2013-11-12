""" Helpers to support json encoding of session data """

from datetime import datetime


def set_last_activity(request, dt):
    """ Set the last activity datetime as a string in the session. """
    request.session['_session_security'] = dt.isoformat()


def get_last_activity(request):
    """
    Get the last activity datetime string from the session and return the
    python datetime object.
    """
    return datetime.strptime(request.session['_session_security'],
        '%Y-%m-%dT%H:%M:%S.%f')
