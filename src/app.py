import os
from utils.file_operations import (
    read_md_file_and_generate_response,
    write_response_to_file,
    display_response
)

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

if __name__ == "__main__":
    main()