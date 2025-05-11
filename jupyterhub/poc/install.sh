# This script installs JupyterHub on a Kubernetes cluster using Helm.
# It creates a namespace for JupyterHub, installs the Helm chart, and applies the configuration.

# default values of the helm chart:
# https://github.com/jupyterhub/zero-to-jupyterhub-k8s

helm upgrade --cleanup-on-fail \
  --install jhub jupyterhub/jupyterhub \
  --namespace jupyterhub --create-namespace \
  --version=4.2.0 \
  --values config.yaml