from prompts.user_prompt import userprompt
from utils.openai_api import call_openai_api
from utils.file_operations import write_response_to_file
from docker_operations.get_info import get_namespaces, get_k8s_info, discovery_file
from utils.file_processor import process_file_or_folder


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
    discovery_file()

    chunks = process_file_or_folder("discovery.json")
    chunks.append({
        "content": f"K8s details {k8s_info}",
        "role": "user"
    })
    chunks.append({
        "content": f"Experiment details {experiment_detail}",
        "role": "user"
    })
    chunks.append({
        "content": userprompt("kubernetes_prompt"),
        "role": "user"
    })
    experiment_file = call_openai_api(chunks)
    print(experiment_file)
    write_response_to_file(experiment_file,f"{experiment_name}.json")
