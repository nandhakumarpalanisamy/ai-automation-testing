import pytest
from unittest.mock import patch
from openai import OpenAIError
from src.clients import generate_answer

def test_api_failure_invalid_model():
    """Simulates an API failure to verify framework handles it correctly (Not an AI quality failure)."""
    with patch("src.clients.get_model_under_test_client") as mock_client:
        mock_client.return_value.chat.completions.create.side_effect = OpenAIError("Invalid model ID or API key missing")
        
        response = generate_answer("Hello")
        
        assert response.startswith("Error generating answer")

def test_api_failure_timeout():
    """Simulates a generic timeout or unexpected infrastructure error."""
    with patch("src.clients.get_model_under_test_client") as mock_client:
        mock_client.return_value.chat.completions.create.side_effect = Exception("Request timed out")
        
        response = generate_answer("Hello")
        
        assert response == "An unexpected error occurred."
