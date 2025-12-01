"""
Tests for question generation endpoint.
"""
import json
from unittest.mock import patch, MagicMock


def test_question_endpoint_returns_200(client):
    """
    Test that question endpoint returns 200 for valid request.
    """
    # Act
    response = client.get('/api/chapters/1/questions/1?language=python')

    # Assert
    assert response.status_code == 200


def test_question_endpoint_invalid_chapter(client):
    """
    Test that question endpoint returns 404 for invalid chapter.
    """
    # Act
    response = client.get('/api/chapters/999/questions/1?language=python')
    data = json.loads(response.data)

    # Assert
    assert response.status_code == 404
    assert 'error' in data


def test_question_endpoint_invalid_level_too_low(client):
    """
    Test that question endpoint returns 400 for level < 1.
    """
    # Act
    response = client.get('/api/chapters/1/questions/0?language=python')
    data = json.loads(response.data)

    # Assert
    assert response.status_code == 400
    assert 'error' in data


def test_question_endpoint_invalid_level_too_high(client):
    """
    Test that question endpoint returns 400 for level > 10.
    """
    # Act
    response = client.get('/api/chapters/1/questions/11?language=python')
    data = json.loads(response.data)

    # Assert
    assert response.status_code == 400
    assert 'error' in data


def test_question_endpoint_returns_correct_structure(client):
    """
    Test that question endpoint returns correct JSON structure.
    """
    # Act
    response = client.get('/api/chapters/1/questions/1?language=python')
    data = json.loads(response.data)

    # Assert
    assert 'question' in data
    assert 'level' in data
    assert 'language' in data
    assert 'chapter_id' in data
    assert 'cached' in data
    assert 'dynamic_chapter' in data


def test_question_content_structure(client):
    """
    Test that question content has all required fields.
    """
    # Act
    response = client.get('/api/chapters/1/questions/1?language=python')
    data = json.loads(response.data)
    question = data['question']

    # Assert
    required_fields = [
        'level', 'problem_id', 'title', 'description', 'examples',
        'hints', 'function_signature', 'test_cases', 'solution',
        'solution_explanation', 'time_complexity', 'space_complexity'
    ]

    for field in required_fields:
        assert field in question, f"Missing field: {field}"

    assert isinstance(question['examples'], list)
    assert isinstance(question['hints'], list)
    assert isinstance(question['test_cases'], list)
    assert data['level'] == 1


def test_question_caching(client):
    """
    Test that questions are cached.
    """
    # Act - First request
    response1 = client.get('/api/chapters/1/questions/1?language=python')
    data1 = json.loads(response1.data)

    # Act - Second request
    response2 = client.get('/api/chapters/1/questions/1?language=python')
    data2 = json.loads(response2.data)

    # Assert
    assert data1['cached'] == False or data1['cached'] == True
    assert data2['cached'] == True
    assert data1['question']['problem_id'] == data2['question']['problem_id']


def test_different_levels_return_different_questions(client):
    """
    Test that different levels return different questions.
    """
    # Act
    response1 = client.get('/api/chapters/1/questions/1?language=python')
    response5 = client.get('/api/chapters/1/questions/5?language=python')

    data1 = json.loads(response1.data)
    data5 = json.loads(response5.data)

    # Assert
    assert data1['level'] == 1
    assert data5['level'] == 5
    # They should have different titles or problem IDs
    assert data1['question']['title'] != data5['question']['title']


@patch('main.OpenAIService.generate_single_question')
def test_question_with_mocked_openai(mock_generate_question, client):
    """
    Test question generation with mocked OpenAI.
    """
    # Arrange
    mock_question = {
        "level": 3,
        "problem_id": "mock_problem_123",
        "title": "Mocked Question",
        "description": "Mocked description",
        "examples": [{"input": "test", "output": "result", "explanation": "explanation"}],
        "hints": ["hint1", "hint2"],
        "function_signature": "def solution():",
        "test_cases": [{"input": "test", "expected_output": "result"}],
        "solution": "def solution(): return True",
        "solution_explanation": "Mocked explanation",
        "time_complexity": "O(1)",
        "space_complexity": "O(1)"
    }
    mock_generate_question.return_value = mock_question

    # Act
    response = client.get('/api/chapters/1/questions/3?language=python')
    data = json.loads(response.data)

    # Assert
    assert response.status_code == 200
    assert data['question']['title'] == "Mocked Question"
    assert data['level'] == 3


def test_question_with_different_languages(client):
    """
    Test that question endpoint works with different languages.
    """
    # Act
    response_python = client.get('/api/chapters/1/questions/1?language=python')
    response_java = client.get('/api/chapters/1/questions/1?language=java')

    data_python = json.loads(response_python.data)
    data_java = json.loads(response_java.data)

    # Assert
    assert response_python.status_code == 200
    assert response_java.status_code == 200
    assert data_python['language'] == 'python'
    assert data_java['language'] == 'java'
    # Function signatures should be different for different languages
    assert data_python['question']['function_signature'] != data_java['question']['function_signature']