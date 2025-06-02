import pytest
import asyncio
from src.utils.openai_api import call_openai_api # Assuming call_openai_api is now async

# It's good practice to keep imports from your own project separate or clearly marked.

@pytest.mark.asyncio
async def test_call_openai_api_success(mocker):
    # Arrange
    mock_get_env_value = mocker.patch('src.utils.openai_api.get_env_value')
    mock_get_env_value.side_effect = lambda key: {
        "GENAI_URL": "http://mockapi.com",
        "GENAI_API_KEY": "mockapikey"
    }.get(key)

    # Mock httpx.AsyncClient for async context manager
    mock_async_client_instance = mocker.MagicMock()
    mock_async_client_instance.post = mocker.AsyncMock() # Crucial: post is an AsyncMock

    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'data': {'content': 'mocked response content'}}
    mock_async_client_instance.post.return_value = mock_response

    # Patch the AsyncClient constructor to return our instance,
    # and configure its __aenter__ to return the instance with the AsyncMock post.
    mock_async_client_constructor = mocker.patch('httpx.AsyncClient')
    mock_async_client_constructor.return_value.__aenter__.return_value = mock_async_client_instance
    
    chunks = [{"content": "test chunk", "role": "user"}]
    
    # Act
    result = await call_openai_api(chunks) # call_openai_api is now async
    
    # Assert
    assert result == 'mocked response content'
    mock_async_client_instance.post.assert_called_once()
    # You might want to assert the call arguments as well if they are important:
    # mock_async_client_instance.post.assert_called_once_with("http://mockapi.com", headers=..., json=...)

@pytest.mark.asyncio
async def test_call_openai_api_failure(mocker):
    # Arrange
    mock_get_env_value = mocker.patch('src.utils.openai_api.get_env_value')
    mock_get_env_value.side_effect = lambda key: {
        "GENAI_URL": "http://mockapi.com",
        "GENAI_API_KEY": "mockapikey"
    }.get(key)

    mock_async_client_instance = mocker.MagicMock()
    mock_async_client_instance.post = mocker.AsyncMock()

    mock_response = mocker.MagicMock()
    mock_response.status_code = 500
    # No need to mock response.json() for failure case if it's not called
    mock_async_client_instance.post.return_value = mock_response

    mock_async_client_constructor = mocker.patch('httpx.AsyncClient')
    mock_async_client_constructor.return_value.__aenter__.return_value = mock_async_client_instance

    chunks = [{"content": "test chunk", "role": "user"}]
    
    # Act
    result = await call_openai_api(chunks) # call_openai_api is now async
    
    # Assert
    assert result == "System not available at this moment."
    mock_async_client_instance.post.assert_called_once()