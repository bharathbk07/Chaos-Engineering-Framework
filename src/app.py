import os
from utils.file_operations import (
    read_md_file_and_generate_response,
    write_response_to_file,
    display_response,
    display_user_selected_exp
)
from docker_operations.k8s_experiment import process_k8s_experiment
from chas_toolkit_exp.exp_validate import validate_experiment

def main():
    readme_path = "/Users/bharathkumarm/Docker/microservices-demo/README.md"
    output_file = "chaos_experiments.json"
    
    if os.path.exists(output_file):
        if os.path.getsize(output_file) > 0:
            print(f"{output_file} exists and is not empty. Displaying response...")
            display_response(output_file)
        else:
            print(f"{output_file} exists but is empty. Generating response...")
            data = read_md_file_and_generate_response(readme_path)
            write_response_to_file(data, output_file)
            display_response(output_file)
    else:
        print(f"{output_file} does not exist. Generating response...")
        data = read_md_file_and_generate_response(readme_path)
        write_response_to_file(data, output_file)
        display_response(output_file)

    print("\n" + "="*50 + " Chaos Experiment Selection " + "="*50 + "\n")
    experiment_name = input("Enter the experiment name: ")

    print("\n" + "="*50 + " User Experiment Details " + "="*50 + "\n")
    experiment_detail = display_user_selected_exp(output_file, experiment_name)
    
    print( "="*40 + "Available Namespaces" +"="*40)
    process_k8s_experiment(output_file, experiment_name, experiment_detail)

    validate_experiment(f"{experiment_name}.json")

if __name__ == "__main__":
    main()
