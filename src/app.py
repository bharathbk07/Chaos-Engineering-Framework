import os
import json
from utils.file_processor import process_file_or_folder
from utils.openai_api import call_openai_api
from prompts.user_prompt import userprompt

def main():
    readme_path = "/Users/bharathkumarm/Docker/wordsmith/README.md"
    chunks = process_file_or_folder(readme_path)
    chunks.append({
        "content": userprompt(),
        "role": "user"
    })
    
    data = call_openai_api(chunks)
    print(data)
    
    # output_file = "chaos_experiments.json"
    # try:
    #     with open(output_file, 'w', encoding='utf-8') as file:
    #         json.dump(data, file, indent=4)
    #     print(f"Chaos experiments saved to {output_file}")
    # except Exception as e:
    #     print(f"Failed to save chaos experiments: {e}")

if __name__ == "__main__":
    main()