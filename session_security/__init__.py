try:
    import unittest_data_provider
except ImportError:
    print '''
    django-session-security tests require: pip install unittest-data-provider
    '''
    raise
