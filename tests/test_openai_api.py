import unittest
from unittest.mock import patch, MagicMock
from src.utils.openai_api import call_openai_api

class TestOpenAIAPI(unittest.TestCase):

    @patch('src.utils.openai_api.requests.post')
    @patch('src.utils.openai_api.get_env_value')
    def test_call_openai_api_success(self, mock_get_env_value, mock_post):
        # Arrange
        mock_get_env_value.side_effect = lambda key: {
            "GENAI_URL": "http://mockapi.com",
            "GENAI_API_KEY": "mockapikey"
        }.get(key)
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {'content': 'mocked response content'}
        }
        mock_post.return_value = mock_response
        
        chunks = [{"content": "test chunk", "role": "user"}]
        
        # Act
        result = call_openai_api(chunks)
        
        # Assert
        self.assertEqual(result, 'mocked response content')
        mock_post.assert_called_once()

    @patch('src.utils.openai_api.requests.post')
    @patch('src.utils.openai_api.get_env_value')
    def test_call_openai_api_failure(self, mock_get_env_value, mock_post):
        # Arrange
        mock_get_env_value.side_effect = lambda key: {
            "GENAI_URL": "http://mockapi.com",
            "GENAI_API_KEY": "mockapikey"
        }.get(key)
        
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        chunks = [{"content": "test chunk", "role": "user"}]
        
        # Act
        result = call_openai_api(chunks)
        
        # Assert
        self.assertEqual(result, "System not available at this moment.")
        mock_post.assert_called_once()

if __name__ == '__main__':
    unittest.main()