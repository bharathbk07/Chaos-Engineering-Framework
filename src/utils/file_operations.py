import json
from utils.file_processor import process_file_or_folder
from utils.openai_api import call_openai_api
from prompts.user_prompt import userprompt

def read_md_file_and_generate_response(readme_path):
    chunks = process_file_or_folder(readme_path)
    chunks.append({
        "content": userprompt("analyze_application"),
        "role": "user"
    })
    return call_openai_api(chunks)

def write_response_to_file(data, output_file):
    try:
        data = json.loads(data) if isinstance(data, str) else data
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        print(f"Chaos experiments saved to {output_file}")
    except Exception as e:
        print(f"Failed to save chaos experiments: {e}")

def read_response_from_file(output_file):
    try:
        with open(output_file, 'r', encoding='utf-8') as file:
            saved_data = json.load(file)
        return saved_data
    except FileNotFoundError:
        print(f"The file {output_file} does not exist.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {output_file}: {e}")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

def display_response(output_file):
    try:
        saved_data = read_response_from_file(output_file)
        
        # If any instance is a string, attempt to parse it as JSON
        if isinstance(saved_data, str):
            saved_data = json.loads(saved_data)

        print(f"{'- Chaos Experiments recommended by AI -':^40}")
        print("-" * 40)
        for item in saved_data:
            if "chaos" in item:
                print(f"- {'Chaos Experiment Title :':25} {item['experiment_title']}")

        print(f"{'\n- Performance Scenario recommended by AI -':^40}")
        print("-" * 40)
        for item in saved_data:
            if "performance" in item: 
                print(f"- {'Performance Scenario Title :':25} {item['scenario_title']}")
 

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {output_file}: {e}")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")

def display_user_selected_exp(output_file, experiment_title):  
    try:
        saved_data = read_response_from_file(output_file)
        
        # If any instance is a string, attempt to parse it as JSON
        if isinstance(saved_data, str):
            saved_data = json.loads(saved_data)
        
        for item in saved_data:
            if "chaos" in item and item['experiment_title'] == experiment_title:
                print("\n=== Chaos Experiment Details ===")
                print(f"{'Experiment Title:':25} {item['experiment_title']}")
                print(f"{'Hypothesis:':25} {item['hypothesis']}")
                print(f"{'Experiment Description:':25} {item['experiment_description']}")
                print(f"{'Expected Outcome:':25} {item['expected_outcome']}")
                print(f"{'Component to be Tested:':25} {item['component_to_be_tested']}")
                print(f"{'Failure Type:':25} {item['failure_type']}")
                print(f"{'Blast Radius:':25} {item['blast_radius']}")
                print(f"{'Rollback Plan:':25} {item['rollback_plan']}")
                print(f"{'Observability Check:':25} {item['observability_check']}")
                print(f"{'Priority:':25} {item['priority']}")
                print(f"{'Test Tool:':25} {item['test_tool']}")
                print(f"{'Metrics to Monitor:':25} {item['metrics_to_monitor']}")
                print("=" * 35)
                return item

            if "performance" in item and item['scenario_title'] == experiment_title:
                print("\n=== Performance Scenario Details ===")
                print(f"{'Scenario Title:':25} {item['scenario_title']}")
                print(f"{'Scenario Description:':25} {item['scenario_description']}")
                print(f"{'User Flow:':25} {item['user_flow']}")
                print(f"{'Expected Outcome:':25} {item['expected_outcome']}")
                print(f"{'Priority:':25} {item['priority']}")
                print(f"{'Observability Check:':25} {item['observability_check']}")
                print(f"{'Test Type:':25} {item['test_type']}")
                print(f"{'Test Tool:':25} {item['test_tool']}")
                print("=" * 35)
                return item

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {output_file}: {e}")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")