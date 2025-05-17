import subprocess
import sys
import json

def is_k8s_running():
    try:
        subprocess.check_output(['kubectl', 'version', '--client'], stderr=subprocess.STDOUT)
        return True
    except Exception:
        return False

def get_namespaces():
    try:
        output = subprocess.check_output(['kubectl', 'get', 'namespaces', '-o', 'json'])
        ns_data = json.loads(output)
        namespaces = [item['metadata']['name'] for item in ns_data['items']]
        return namespaces
    except Exception as e:
        print(f"Error fetching namespaces: {e}")
        return []

def get_namespace_details(namespace):
    details = {}
    try:
        # Get labels
        ns_info = subprocess.check_output(['kubectl', 'get', 'namespace', namespace, '-o', 'json'])
        ns_json = json.loads(ns_info)
        details['labels'] = ns_json['metadata'].get('labels', {})

        # Get services
        svc_info = subprocess.check_output(['kubectl', 'get', 'svc', '-n', namespace, '-o', 'json'])
        svc_json = json.loads(svc_info)
        details['services'] = [item['metadata']['name'] for item in svc_json['items']]

        # Get pods
        pod_info = subprocess.check_output(['kubectl', 'get', 'pods', '-n', namespace, '-o', 'json'])
        pod_json = json.loads(pod_info)
        details['pods'] = [item['metadata']['name'] for item in pod_json['items']]

        # Get deployments
        dep_info = subprocess.check_output(['kubectl', 'get', 'deployments', '-n', namespace, '-o', 'json'])
        dep_json = json.loads(dep_info)
        details['deployments'] = [item['metadata']['name'] for item in dep_json['items']]

    except Exception as e:
        print(f"Error fetching details for namespace '{namespace}': {e}")
    return details

def get_k8s_info(user_ns):
    if not is_k8s_running():
        print("Kubernetes is not running or kubectl is not configured.")
        sys.exit(1)

    namespaces = get_namespaces()

    if not namespaces and user_ns not in namespaces:
        print("No namespaces found.")
        sys.exit(1)

    details = get_namespace_details(user_ns)
    details['namespace'] = user_ns
    return (json.dumps(details, indent=2))
