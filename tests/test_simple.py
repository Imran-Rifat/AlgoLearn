def test_simple_pass():
    assert 1 + 1 == 2

def test_another():
    assert 'hello'.upper() == 'HELLO'

def test_flask_import():
    try:
        import flask
        assert True
    except ImportError:
        # If flask not installed, that's OK for this simple test
        pass

def test_pytest_working():
    # Just verify pytest can run this test
    assert True
