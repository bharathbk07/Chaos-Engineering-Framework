import os
from dotenv import load_dotenv, find_dotenv

def get_env_value(key, env_file='.env'):
    """
    Fetches the value of a key from a .env file or the current shell session.

    :param key: The environment variable key to fetch.
    :param env_file: Path to the .env file (default is '.env').
    :return: The value of the environment variable or None if the key is not found.
    """
    
    # Attempt to load the .env file if it exists
    if os.path.exists(env_file):
        load_dotenv(dotenv_path=env_file)
    else:
        # Use the default search mechanism for a .env file if not explicitly provided
        load_dotenv(find_dotenv())

    # Fetch the value of the key, either from the .env file or the shell environment
    return os.getenv(key)