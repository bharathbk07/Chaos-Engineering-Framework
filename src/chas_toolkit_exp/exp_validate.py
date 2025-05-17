from utils.file_operations import write_response_to_file, read_response_from_file
from utils.openai_api import call_openai_api
from prompts.user_prompt import userprompt
from utils.file_processor import process_file_or_folder
import subprocess
import time

def validate_experiment(file_name):
    """
    Validate the experiment by reading the response from a file.
    
    Args:
        file_name (str): The name of the file to read the response from.
    
    Returns:
        dict: The content of the file as a dictionary.
    """
    try:
        output = subprocess.check_output(
            ['chaos', 'validate', f'{file_name}'],
            stderr=subprocess.STDOUT
        )
        decoded_output = output.decode('utf-8').strip()
        print(decoded_output)
        valid_phrases = [
            "experiment syntax and semantic look valid",
            "Experiment looks valid"
        ]
        if not any(phrase in decoded_output for phrase in valid_phrases):
            fix_experiment(file_name, decoded_output)
            print(f"The experiment file is not valid. Error message: {decoded_output}")
            
    except subprocess.CalledProcessError as e:
        print(f"The experiment file is not valid. Error: {e.output.decode('utf-8')}")
        fix_experiment(file_name, e.output.decode('utf-8'))
        time.sleep(10)
        validate_experiment(file_name)
    except FileNotFoundError:
        print("Error: 'chaos' command not found. Please ensure Chaos Toolkit is installed and in your PATH.")

def fix_experiment(file_name, error_message):
    # Read the response from the specified file
    print(f"Fixing the experiment file: {file_name}")
    chunks = process_file_or_folder(file_name)
    chunks.append({
        "content": f"Experiment file error message {error_message}",
        "role": "user"
    })
    chunks.append({
        "content": userprompt("kubernetes_prompt"),
        "role": "user"
    })
    experiment_file = call_openai_api(chunks)
    write_response_to_file(experiment_file, file_name)