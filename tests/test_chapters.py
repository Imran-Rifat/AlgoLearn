"""
Tests for chapters endpoint with dynamic OpenAI generation.
"""
import json
from unittest.mock import MagicMock, patch


def test_chapters_endpoint_returns_200(client):
    """
    Test that chapters endpoint returns 200 status code.
    """
    # Act
    response = client.get('/api/chapters?language=python')

    # Assert
    assert response.status_code == 200


def test_chapters_endpoint_requires_language(client):
    """
    Test that chapters endpoint requires language parameter.
    """
    # Act
    response = client.get('/api/chapters')
    data = json.loads(response.data)

    # Assert
    assert response.status_code == 200  # Should default to python
    assert 'language' in data
    assert data['language'] == 'python'


def test_chapters_endpoint_returns_correct_structure(client):
    """
    Test that chapters endpoint returns correct JSON structure.
    """
    # Act
    response = client.get('/api/chapters?language=python')
    data = json.loads(response.data)

    # Assert
    assert 'chapters' in data
    assert 'language' in data
    assert 'total_chapters' in data
    assert 'min_level' in data
    assert 'max_level' in data
    assert 'dynamic' in data
    assert data['dynamic'] == True


def test_chapters_are_list(client):
    """
    Test that chapters are returned as a list.
    """
    # Act
    response = client.get('/api/chapters?language=python')
    data = json.loads(response.data)

    # Assert
    assert isinstance(data['chapters'], list)


def test_chapter_structure(client):
    """
    Test that each chapter has required fields.
    """
    # Act
    response = client.get('/api/chapters?language=python')
    data = json.loads(response.data)

    # Assert
    if len(data['chapters']) > 0:
        chapter = data['chapters'][0]
        assert 'id' in chapter
        assert 'name' in chapter
        assert 'topics' in chapter
        assert 'difficulty_levels' in chapter
        assert isinstance(chapter['id'], int)
        assert isinstance(chapter['name'], str)
        assert isinstance(chapter['topics'], list)
        assert chapter['difficulty_levels'] == 10


def test_chapters_with_unsupported_language(client):
    """
    Test that chapters endpoint returns error for unsupported language.
    """
    # Act
    response = client.get('/api/chapters?language=unsupported')
    data = json.loads(response.data)

    # Assert
    assert response.status_code == 400
    assert 'error' in data


def test_chapters_force_refresh(client):
    """
    Test that force_refresh parameter works.
    """
    # Act
    response = client.get('/api/chapters?language=python&force_refresh=true')
    data = json.loads(response.data)

    # Assert
    assert response.status_code == 200
    assert 'cached' in data


@patch('main.openai.ChatCompletion.create')
def test_chapters_with_mocked_openai(mock_openai_create, client):
    """
    Test chapters generation with mocked OpenAI.
    """
    # Arrange
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = json.dumps([
        {
            "id": 1,
            "name": "Mocked Chapter",
            "topics": ["topic1", "topic2"],
            "difficulty_levels": 10
        }
    ])
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_openai_create.return_value = mock_response

    # Act
    response = client.get('/api/chapters?language=python&force_refresh=true')
    data = json.loads(response.data)

    # Assert
    assert response.status_code == 200
    assert len(data['chapters']) > 0
    assert data['chapters'][0]['name'] == "Mocked Chapter"


def test_chapters_min_max_levels(client):
    """
    Test that min and max levels are correctly returned.
    """
    # Act
    response = client.get('/api/chapters?language=python')
    data = json.loads(response.data)

    # Assert
    assert data['min_level'] == 1
    assert data['max_level'] == 10
