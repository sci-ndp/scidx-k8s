#!/usr/bin/env python3

import os
import time
from kubernetes import client, config
import yaml
from pathlib import Path


def load_yaml_file(file_path):
    """
    Load a YAML file and return a list of its contents (supports multi-document YAML).
    """
    with open(file_path, 'r') as f:
        return list(yaml.safe_load_all(f))  # Convert iterator to list for easier handling

def wait_for_namespace(api_instance, namespace, timeout=60):
    """
    Wait until the specified namespace is available.
    """
    print(f"Waiting for namespace '{namespace}' to be available...")
    start_time = time.time()
    while True:
        try:
            api_instance.read_namespace(name=namespace)
            print(f"Namespace '{namespace}' is ready")
            return True
        except client.ApiException as e:
            if e.status == 404:
                if time.time() - start_time > timeout:
                    raise Exception(f"Timeout waiting for namespace '{namespace}' to be created")
                time.sleep(1)
            else:
                raise e

def apply_manifest(api_client, manifest, namespace=None):
    """
    Apply a Kubernetes manifest using the appropriate API.
    """
    if manifest is None:  # Skip empty documents
        return
    kind = manifest.get('kind')
    api_version = manifest.get('apiVersion')
    metadata = manifest.get('metadata', {})
    name = metadata.get('name')

    print(f"Applying {kind} '{name}'...")

    if kind == 'Namespace':
        v1 = client.CoreV1Api(api_client)
        v1.create_namespace(body=manifest)
    elif kind == 'Deployment':
        apps_v1 = client.AppsV1Api(api_client)
        apps_v1.create_namespaced_deployment(namespace=namespace, body=manifest)
    elif kind == 'Service':
        v1 = client.CoreV1Api(api_client)
        v1.create_namespaced_service(namespace=namespace, body=manifest)
    elif kind == 'ConfigMap':
        v1 = client.CoreV1Api(api_client)
        v1.create_namespaced_config_map(namespace=namespace, body=manifest)
    elif kind == 'Role':
        rbac_v1 = client.RbacAuthorizationV1Api(api_client)
        rbac_v1.create_namespaced_role(namespace=namespace, body=manifest)
    elif kind == 'RoleBinding':
        rbac_v1 = client.RbacAuthorizationV1Api(api_client)
        rbac_v1.create_namespaced_role_binding(namespace=namespace, body=manifest)
    elif kind == 'Ingress':
        networking_v1 = client.NetworkingV1Api(api_client)
        networking_v1.create_namespaced_ingress(namespace=namespace, body=manifest)
    else:
        print(f"Skipping unsupported kind: {kind}")
        return

    print(f"Successfully applied {kind} '{name}'")


def get_loadbalancer_url(api_instance, namespace, service_name="nginx-ingress-ingress-nginx-controller", timeout=300):
    """
    Wait for and retrieve the external IP or hostname of the nginx-ingress-controller LoadBalancer service.
    Returns the access URL with /dspaces path.
    """
    print(f"Waiting for LoadBalancer endpoint for service '{service_name}' in namespace '{namespace}'...")
    start_time = time.time()
    while True:
        try:
            service = api_instance.read_namespaced_service(name=service_name, namespace=namespace)
            if service.status.load_balancer.ingress:
                ingress = service.status.load_balancer.ingress[0]
                # Check for either IP or hostname
                if ingress.ip:
                    endpoint = ingress.ip
                elif ingress.hostname:
                    endpoint = ingress.hostname
                else:
                    raise Exception(f"No valid IP or hostname found in LoadBalancer ingress for '{service_name}'")
                url = f"http://{endpoint}/dspaces"
                print(f"LoadBalancer URL is ready: {url}")
                return url
            if time.time() - start_time > timeout:
                raise Exception(f"Timeout waiting for LoadBalancer endpoint for '{service_name}'")
            time.sleep(5)
        except client.ApiException as e:
            if e.status == 404:
                raise Exception(f"Service '{service_name}' not found in namespace '{namespace}'")
            else:
                raise e

# ---------------------------------------------------------------------------------------
def main():
    """
    Main function to deploy Kubernetes resources from YAML manifests.

    Steps:
    1. Load the kubeconfig to configure access to the Kubernetes cluster.
    2. Apply the namespace manifest (dspaces-namespace.yaml) if it exists.
    3. Wait for the namespace to be ready.
    4. Apply all other YAML manifests in the same directory, skipping the namespace file.
    """
    # Load kubeconfig (assumes kubectl is configured)
    try:
        config.load_kube_config()
    except Exception as e:
        raise Exception(f"Failed to load kubeconfig: {e}")

    # Initialize Kubernetes API client
    api_client = client.ApiClient()
    # Define the directory containing manifests (move up to dspaces directory)
    manifest_dir = Path(__file__).parent.parent # Go up two levels: python -> dspaces
    namespace_file = manifest_dir / 'dspaces-namespace.yaml'

    # Apply the namespace
    if namespace_file.exists():
        namespace_manifests = load_yaml_file(namespace_file)  # List of documents
        if not namespace_manifests or namespace_manifests[0] is None:
            raise ValueError("dspaces-namespace.yaml is empty or invalid")
        namespace_manifest = namespace_manifests[0]  # Assume namespace is the first/only document
        ns = namespace_manifest['metadata']['name']
        try:
            apply_manifest(api_client, namespace_manifest)
        except client.ApiException as e:
            if e.status == 409:  # Conflict means it already exists
                print(f"Namespace '{ns}' already exists, proceeding...")
            else:
                raise e
    else:
        raise FileNotFoundError("dspaces-namespace.yaml not found")

    # Wait for namespace to be ready
    v1_api = client.CoreV1Api(api_client)
    wait_for_namespace(v1_api, ns)

    # Apply all other manifests in the directory
    errors = []
    # Iterate over all files in the directory
    for file_path in manifest_dir.glob('*.yaml'):
        if file_path.name == 'dspaces-namespace.yaml':
            continue  # Skip the namespace file as it's already applied
        manifests = load_yaml_file(file_path)
        # Apply each manifest in each YAML file
        for manifest in manifests:
            if manifest is None:  # Skip empty documents
                continue
            try:
                apply_manifest(api_client, manifest, namespace=ns)
            except client.ApiException as e:
                if e.status == 409:
                    print(f"Resource '{manifest['metadata']['name']}' in '{file_path.name}' already exists, skipping...")
                else:
                    errors.append(f"Error applying '{file_path.name}': {e}")

    if errors:
        print("Deployment completed with errors:")
        for error in errors:
            print(error)
        exit(1)
    
    access_url = get_loadbalancer_url(v1_api, 'ingress-nginx')
    print(f"Access the dspaces at: {access_url}")
    return access_url

# ---------------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Deployment failed: {e}")
        exit(1)
    print("Deployment completed successfully")