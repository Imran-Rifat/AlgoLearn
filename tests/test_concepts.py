"""
Tests for concept content endpoint.
"""
import json
from unittest.mock import patch, MagicMock


def test_concept_endpoint_returns_200(client):
    """
    Test that concept endpoint returns 200 for valid chapter.
    """
    # Act
    response = client.get('/api/chapters/1/concept?language=python')

    # Assert
    assert response.status_code == 200


def test_concept_endpoint_requires_valid_chapter(client):
    """
    Test that concept endpoint returns 404 for invalid chapter.
    """
    # Act
    response = client.get('/api/chapters/999/concept?language=python')
    data = json.loads(response.data)

    # Assert
    assert response.status_code == 404
    assert 'error' in data


def test_concept_endpoint_returns_correct_structure(client):
    """
    Test that concept endpoint returns correct JSON structure.
    """
    # Act
    response = client.get('/api/chapters/1/concept?language=python')
    data = json.loads(response.data)

    # Assert
    assert 'concept' in data
    assert 'language' in data
    assert 'chapter_id' in data
    assert 'cached' in data
    assert 'dynamic_chapter' in data


def test_concept_content_structure(client):
    """
    Test that concept content has required fields.
    """
    # Act
    response = client.get('/api/chapters/1/concept?language=python')
    data = json.loads(response.data)
    concept = data['concept']

    # Assert
    assert 'title' in concept
    assert 'overview' in concept
    assert 'theory_content' in concept
    assert 'learning_objectives' in concept
    assert 'code_examples' in concept
    assert 'key_takeaways' in concept
    assert isinstance(concept['learning_objectives'], list)
    assert isinstance(concept['code_examples'], list)
    assert isinstance(concept['key_takeaways'], list)


def test_concept_caching(client):
    """
    Test that concept content is cached.
    """
    # Act - First request
    response1 = client.get('/api/chapters/1/concept?language=python')
    data1 = json.loads(response1.data)

    # Act - Second request (should be cached)
    response2 = client.get('/api/chapters/1/concept?language=python')
    data2 = json.loads(response2.data)

    # Assert
    assert data1['cached'] == False or data1['cached'] == True
    assert data2['cached'] == True
    assert data1['concept']['title'] == data2['concept']['title']


def test_concept_with_different_languages(client):
    """
    Test that concept endpoint works with different languages.
    """
    # Act
    response_python = client.get('/api/chapters/1/concept?language=python')
    response_java = client.get('/api/chapters/1/concept?language=java')

    data_python = json.loads(response_python.data)
    data_java = json.loads(response_java.data)

    # Assert
    assert response_python.status_code == 200
    assert response_java.status_code == 200
    assert data_python['language'] == 'python'
    assert data_java['language'] == 'java'
    # Concepts might be different for different languages
    assert data_python['concept']['title'] != data_java['concept']['title']


@patch('main.OpenAIService.generate_concept_content')
def test_concept_with_mocked_openai(mock_generate_concept, client):
    """
    Test concept generation with mocked OpenAI.
    """
    # Arrange
    mock_concept = {
        "title": "Mocked Concept",
        "overview": "Mocked overview",
        "theory_content": "<h2>Mocked</h2>",
        "learning_objectives": ["obj1", "obj2"],
        "code_examples": [{"code": "mock code", "explanation": "mock explanation"}],
        "key_takeaways": ["takeaway1", "takeaway2"]
    }
    mock_generate_concept.return_value = mock_concept

    # Act
    response = client.get('/api/chapters/1/concept?language=python')
    data = json.loads(response.data)

    # Assert
    assert response.status_code == 200
    assert data['concept']['title'] == "Mocked Concept"


def test_concept_endpoint_without_language_defaults_to_python(client):
    """
    Test that concept endpoint defaults to Python when language not specified.
    """
    # Act
    response = client.get('/api/chapters/1/concept')
    data = json.loads(response.data)

    # Assert
    assert response.status_code == 200
    assert data['language'] == 'python'