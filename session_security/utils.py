""" Helpers to support json encoding of session data """

from datetime import datetime


def set_last_activity(session, dt):
    """ Set the last activity datetime as a string in the session. """
    session['_session_security'] = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')


def get_last_activity(session):
    """
    Get the last activity datetime string from the session and return the
    python datetime object.
    """
    try:
        return datetime.strptime(session['_session_security'],
                '%Y-%m-%dT%H:%M:%S.%f')
    except AttributeError:
        #################################################################
        # * this is an odd bug in python
        # bug report: http://bugs.python.org/issue7980
        # bug explained here:
        # http://code-trick.com/python-bug-attribute-error-_strptime/
        # * sometimes, in multithreaded enviroments, we get AttributeError
        #     in this case, we just return datetime.now(),
        #     so that we are not logged out
        #   "./session_security/middleware.py", in update_last_activity
        #     last_activity = get_last_activity(request.session)
        #   "./session_security/utils.py", in get_last_activity
        #     '%Y-%m-%dT%H:%M:%S.%f')
        #   AttributeError: _strptime
        #
        #################################################################

        return datetime.now()
    except TypeError:
        return datetime.now()

