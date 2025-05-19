import subprocess
import time
from utils.file_operations import write_response_to_file, read_json_file
from utils.openai_api import call_openai_api
from prompts.user_prompt import userprompt
from utils.file_processor import process_file_or_folder

def validate_experiment(file_name, fix_count=1):
    """
    Validate the experiment by reading the response from a file.

    Args:
        file_name (str): The name of the file to read the response from.

    Returns:
        None
    """
    valid_phrases = [
        "experiment syntax and semantic look valid",
        "Experiment looks valid"
    ]
    
    try:
        output = subprocess.check_output(
            ['chaos', 'validate', file_name],
            stderr=subprocess.STDOUT
        ).decode('utf-8').strip()
        print(f"Validation output: {output}")

        if not any(phrase in output for phrase in valid_phrases):
            print(f"The experiment file is not valid. Error message: {output}")
            fix_experiment(f"{file_name}", output)

    except subprocess.CalledProcessError as e:
        error_msg = e.output.decode('utf-8')
        print(f"The experiment file is not valid. Error: {error_msg}")
        print("Attempting to fix the experiment file...Try number of fixes: ", fix_count)
        fix_count += 1
        fix_experiment(f"{file_name}", error_msg)
        time.sleep(20)

        try:
            validate_experiment(file_name,fix_count)
        except Exception as retry_err:
            print(f"Retry failed: {retry_err}")
            
    except FileNotFoundError:
        print("Error: 'chaos' command not found. Please ensure Chaos Toolkit is installed and in your PATH.")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

def fix_experiment(file_name, error_message):
    """
    Attempt to fix the experiment file using OpenAI API based on the error message.

    Args:
        file_name (str): The name of the file to fix.
        error_message (str): The error message to provide context.

    Returns:
        None
    """
    try:
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
        chunks.extend(process_file_or_folder("./src/prompts/output.txt"))
       
        experiment_file = call_openai_api(chunks)
        write_response_to_file(experiment_file, file_name)
    except Exception as ex:
        print(f"Failed to fix the experiment file: {ex}")