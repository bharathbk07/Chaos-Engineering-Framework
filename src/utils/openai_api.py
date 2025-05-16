from utils.env_loader import get_env_value
import requests
import json
def call_openai_api(chunks):
    completion_endpoint = get_env_value("GENAI_URL")

    headers = {
        'Content-Type': "application/json",
        'Accept': "text/event-stream, application/json",
        'Authorization': "Bearer " + get_env_value("GENAI_API_KEY")
    }

    payload = {
        "messages": [  
            *chunks,
        ],
        "skill_parameters": {  
            "model_name": "gpt-4o",  
            "emb_type": "openai", 
            "max_output_tokens": 4096 
        },
        "stream_response": False 
    }
    
    response = requests.post(completion_endpoint, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            response_data = response.json()
            return response_data['data']['content']
        except KeyError:
            print("The key 'data' or 'content' does not exist in the response.")
        except json.JSONDecodeError:
            print("Failed to decode the response as JSON.")
    else:
        return "System not available at this moment."