"""
Tests for health check endpoint.
"""
import json


def test_health_endpoint_returns_200(client):
    """
    Test that health endpoint returns 200 status code.
    """
    # Act
    response = client.get('/api/health')

    # Assert
    assert response.status_code == 200


def test_health_endpoint_returns_json(client):
    """
    Test that health endpoint returns JSON.
    """
    # Act
    response = client.get('/api/health')
    data = json.loads(response.data)

    # Assert
    assert response.content_type == 'application/json'
    assert 'status' in data
    assert data['status'] == 'healthy'


def test_health_endpoint_includes_openai_status(client, mock_openai_service):
    """
    Test that health endpoint includes OpenAI connection status.
    """
    # Act
    response = client.get('/api/health')
    data = json.loads(response.data)

    # Assert
    assert 'openai_connected' in data
    assert isinstance(data['openai_connected'], bool)


def test_health_endpoint_includes_supported_languages(client):
    """
    Test that health endpoint includes supported languages.
    """
    # Act
    response = client.get('/api/health')
    data = json.loads(response.data)

    # Assert
    assert 'supported_languages' in data
    assert isinstance(data['supported_languages'], list)
    assert len(data['supported_languages']) > 0


def test_health_endpoint_includes_cache_size(client):
    """
    Test that health endpoint includes cache size.
    """
    # Act
    response = client.get('/api/health')
    data = json.loads(response.data)

    # Assert
    assert 'cache_size' in data
    assert isinstance(data['cache_size'], int)