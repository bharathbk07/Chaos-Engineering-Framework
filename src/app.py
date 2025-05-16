import json
from utils.file_processor import process_file_or_folder
from utils.openai_api import call_openai_api
from prompts.user_prompt import userprompt
import pandas as pd

def main():
    readme_path = "/Users/bharathkumarm/Docker/microservices-demo/README.md"
    chunks = process_file_or_folder(readme_path)
    chunks.append({
        "content": userprompt(),
        "role": "user"
    })
    
    data = call_openai_api(chunks)

    output_file = "chaos_experiments.json"
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
        print(f"Chaos experiments saved to {output_file}")
    except Exception as e:
        print(f"Failed to save chaos experiments: {e}")

    # try:
    #     with open(output_file, 'r', encoding='utf-8') as file:
    #         saved_data = json.load(file)
    #     print("Successfully read the output file.")
        
    #     # If any instance is a string, attempt to parse it as JSON
    #     if isinstance(saved_data, str):
    #         saved_data = json.loads(saved_data)
    #         print("Converted string data to JSON.")
    # except FileNotFoundError:
    #     print(f"The file {output_file} does not exist.")
    # except json.JSONDecodeError as e:
    #     print(f"Error decoding JSON from {output_file}: {e}")
    # except Exception as e:
    #     print(f"An error occurred while reading the file: {e}")
    print(type(data))
    saved_data = json.loads(data)
    try:
       for item in saved_data:
            if "chaos" in item:
                print('-'*50)
                print(f"Experiment Title: {item['experiment_title']}")
                print(f"Hypothesis: {item['hypothesis']}")
                print(f"Experiment Description: {item['experiment_description']}")
                print(f"Expected Outcome: {item['expected_outcome']}")
                print(f"Component to be Tested: {item['component_to_be_tested']}")
                print(f"Failure Type: {item['failure_type']}")
                print(f"Blast Radius: {item['blast_radius']}")
                print(f"Rollback Plan: {item['rollback_plan']}")
                print(f"Observability Check: {item['observability_check']}")
                print(f"Priority: {item['priority']}")
                print(f"Test Tool: {item['test_tool']}")
                print(f"Metrics to Monitor: {item['metrics_to_monitor']}")
                print('-'*50)
            elif "performance" in item: 
                print('-'*50)
                print(f"Scenario Title: {item['scenario_title']}")
                print(f"Scenario Description: {item['scenario_description']}")
                print(f"User Flow: {item['user_flow']}")
                print(f"Expected Outcome: {item['expected_outcome']}")
                print(f"Priority: {item['priority']}")
                print(f"Observability Check: {item['observability_check']}")
                print(f"Test Type: {item['test_type']}")
                print(f"Test Tool: {item['test_tool']}")
                print('-'*50)
    except KeyError as e:   
        print(f"Key error: {e}. Please check the structure of the JSON data.")
    except json.JSONDecodeError as e:           
        print(f"JSON decode error: {e}. Please check the JSON format.")
    except Exception as e:
        print(f"Failed to read or display chaos experiments: {e}")

if __name__ == "__main__":
    main()