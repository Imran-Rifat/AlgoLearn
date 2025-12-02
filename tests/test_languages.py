"""
Tests for languages endpoint.
"""
import json


def test_languages_endpoint_returns_200(client):
    """
    Test that languages endpoint returns 200 status code.
    """
    # Act
    response = client.get('/api/languages')

    # Assert
    assert response.status_code == 200


def test_languages_endpoint_returns_correct_structure(client):
    """
    Test that languages endpoint returns correct JSON structure.
    """
    # Act
    response = client.get('/api/languages')
    data = json.loads(response.data)

    # Assert
    assert 'languages' in data
    assert 'default' in data
    assert 'count' in data
    assert isinstance(data['languages'], list)
    assert isinstance(data['default'], str)
    assert isinstance(data['count'], int)


def test_languages_includes_python(client):
    """
    Test that languages list includes Python.
    """
    # Act
    response = client.get('/api/languages')
    data = json.loads(response.data)

    # Assert
    assert 'python' in data['languages']


def test_default_language_is_python(client):
    """
    Test that default language is Python.
    """
    # Act
    response = client.get('/api/languages')
    data = json.loads(response.data)

    # Assert
    assert data['default'] == 'python'


def test_count_matches_languages_length(client):
    """
    Test that count matches languages list length.
    """
    # Act
    response = client.get('/api/languages')
    data = json.loads(response.data)

    # Assert
    assert data['count'] == len(data['languages'])