import os
from utils.file_operations import (
    read_md_file_and_generate_response,
    write_response_to_file,
    display_response
)
from docker_operations.get_info import get_k8s_info

def main():
    readme_path = "/Users/bharathkumarm/Docker/microservices-demo/README.md"
    output_file = "chaos_experiments.json"
    namespace = "online-store"  # Replace with your desired namespace

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
    
    # Get Kubernetes information
    k8s_info = get_k8s_info(namespace)
    if k8s_info:
        print('-'*40)
        print(k8s_info)
    else:
        print(f"No information found for namespace '{namespace}'.")

if __name__ == "__main__":
    main()