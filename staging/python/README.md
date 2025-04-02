# Temp doc of k8s deployment python script

This is a temporary document/memo for deploying dspaces api and server using the python script `dspaces_k8s_deploy.py`. Currently, the Python k8s client still relies on the local kubeconfig. There will be further updates.




### 1. Create a Virtual Environment
Create a Python virtual environment in the **dspaces/python/** directory to isolate dependencies:
```sh
python3 -m venv venv
```
This creates a venv folder in dspaces/ with an isolated Python environment.

### 2. Activate the Virtual Environment
Activate the virtual environment. From the dspaces/python/ directory, run:
```sh
source venv/bin/activate
```
Terminal prompt will show (venv) to indicate the environment is active.

### 3. Install Dependencies
Install the required Python packages listed in requirements.txt:
```sh
pip install -r requirements.txt
```
This installs the kubernetes package and its dependencies, necessary for interacting with Kubernetes.

### 4. Deploy to Kubernetes
Run the deployment script to apply Kubernetes manifests:
```sh
python python/dspaces_k8s_deploy.py
```

This script deploys k8s manifests defined in the YAML files in **dspaces/**.

Note: current setup uses kubectl with access to your k8s cluster (e.g., ~/.kube/config is set up correctly). Further updated is needed.



### Clean up
Delete k8s resources
```sh
kubectl delete ns dspaces
```
Deactivate the Virtual Environment
```sh
deactivate
```