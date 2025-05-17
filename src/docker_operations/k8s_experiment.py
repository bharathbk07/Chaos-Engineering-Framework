from docker_operations.get_info import get_k8s_info
from prompts.user_prompt import userprompt
from utils.openai_api import call_openai_api
from utils.file_operations import display_user_selected_exp, write_response_to_file
from docker_operations.get_info import get_namespaces
import json

def process_k8s_experiment(output_file, experiment_name, experiment_detail):
    # Get Kubernetes information
    namespaces = get_namespaces()
    if not namespaces:
        print("No namespaces found.")
    else:
        print("Available namespaces:")
        for ns in namespaces:
            print(f"- {ns}")

    print( "="*40 + "Namespaces Selection" + "="*40)
    namespace = input("Enter the Kubernetes namespace: ")

    k8s_info = get_k8s_info(namespace)
    user_details_for_k8s = [
        {
            "content": f"K8s details {k8s_info}",
            "role": "user"
        },
        {
            "content": f"Experiment details {experiment_detail}",
            "role": "user"
        },
        {
            "content": userprompt("kubernetes_prompt"),
            "role": "assistant"
        }
    ]

    write_response_to_file(call_openai_api(user_details_for_k8s),f"{experiment_name}.json")
