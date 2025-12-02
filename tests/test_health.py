def test_health():
    # Simple test that always passes
    assert True
    
def test_flask_exists():
    try:
        import flask
        assert True
    except ImportError:
        # Mark as skipped if flask not installed
        import pytest
        pytest.skip("Flask not installed")
