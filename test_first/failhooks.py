from test_first import test_first_exception

try:
    import pytest
except ImportError:
    pytest = None

def _fail_py_test( exceptionFactory, message ):
    return pytest.fail( message )

def _fail_raise( exceptionFactory, message ):
    raise exceptionFactory( message )


if pytest is None:
    _fail = _fail_raise
else:
    _fail = _fail_py_test

def setMode( mode ):
    FAILS = { 'pytest': _fail_py_test,
               'raise':  _fail_raise }
    global _fail
    _fail = FAILS[ mode ]

def error( message ):
    raise test_first_exception.TestFirstError( message )

def fail( exceptionFactory, message ):
    return _fail( exceptionFactory, f'\ntest_first: {exceptionFactory.__name__}\n'
                                    f'test_first details:\n'
                                    f'{message}' )
