import os
import asyncio
from utils.file_operations import (
    read_md_file_and_generate_response,
    write_response_to_file,
    display_response,
    display_user_selected_exp
)
from docker_operations.k8s_experiment import process_k8s_experiment
from chas_toolkit_exp.exp_validate import validate_experiment
from utils.display import display_framework_info

async def generate_or_display_response(readme_path, output_file):
    try:
        if os.path.exists(output_file):
            if os.path.getsize(output_file) > 0:
                print(f"\n{output_file} exists and is not empty. Displaying list of experiments...\n")
                display_response(output_file)
            else:
                print(f"\n{output_file} exists but is empty. Generating response...\n")
                data = await read_md_file_and_generate_response(readme_path)
                write_response_to_file(data, output_file)
                display_response(output_file)
        else:
            print(f"\n{output_file} does not exist. Generating response...\n")
            data = await read_md_file_and_generate_response(readme_path)
            write_response_to_file(data, output_file)
            display_response(output_file)
            
    except Exception as e:
        print(f"Error in generating or displaying response: {e}")

async def select_experiment(output_file, readme_path):
    try:
        print("\n" + "="*50 + " Chaos Experiment Selection " + "="*50 + "\n")
        experiment_name = None
        experiment_detail = None
        while True:
            experiment_name = input("Enter the experiment name: ")
            print("\n" + "="*50 + " User Experiment Details " + "="*50 + "\n")
            experiment_detail = display_user_selected_exp(output_file, experiment_name)
            choice = input("Do you want to view another experiment? (y/N): ").strip().lower()
            if choice != 'y':
                print("\nReturning the last selected experiment for further processing.\n")
                break
            else:
                await generate_or_display_response(readme_path, output_file)
        # Return the last selected experiment name and detail for further processing
        return experiment_name, experiment_detail

    except Exception as e:
        print(f"Error in selecting experiment: {e}")
        return None, None

def process_and_validate_experiment(output_file, experiment_name, experiment_detail):
    try:
        print("="*40 + "Available Namespaces" + "="*40)
        process_k8s_experiment(output_file, experiment_name, experiment_detail)
        validate_experiment(f"{experiment_name}.json")
    except Exception as e:
        print(f"Error in processing or validating experiment: {e}")

async def main():
    display_framework_info()
    readme_path = "/Users/bharathkumarm/Docker/microservices-demo/README.md"
    output_file = "chaos_experiments.json"

    await generate_or_display_response(readme_path, output_file)
    experiment_name, experiment_detail = await select_experiment(output_file, readme_path)
    print(f"Selected Experiment Name: {experiment_name}")

    if experiment_name and experiment_detail:
        process_and_validate_experiment(output_file, experiment_name, experiment_detail)

if __name__ == "__main__":
    asyncio.run(main())
