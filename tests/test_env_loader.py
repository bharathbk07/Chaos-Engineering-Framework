import os
import pytest
from src.utils.env_loader import get_env_value

def test_get_env_value_existing_key():
    os.environ['TEST_KEY'] = 'test_value'
    assert get_env_value('TEST_KEY') == 'test_value'

def test_get_env_value_non_existing_key():
    assert get_env_value('NON_EXISTING_KEY') is None

def test_get_env_value_with_env_file(monkeypatch):
    with open('.env', 'w') as f:
        f.write('TEST_KEY_FROM_FILE=test_value_from_file\n')
    
    monkeypatch.setattr('os.path.exists', lambda x: True)
    assert get_env_value('TEST_KEY_FROM_FILE') == 'test_value_from_file'

def test_get_env_value_with_no_env_file(monkeypatch):
    monkeypatch.setattr('os.path.exists', lambda x: False)
    assert get_env_value('NON_EXISTING_KEY') is None