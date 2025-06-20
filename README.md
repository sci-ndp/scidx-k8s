# SciDX Kubernetes Resources

This repository provides Kubernetes manifests and supporting files for deploying and managing the SciDX services stack.

## Deployment

Follow these steps to deploy SciDX software stack on Kubernetes cluster:

1. [**Install the NGINX Ingress Controller**](./nginx-ingress-controller/)

2. [**Deploy Kafka Cluster**](./streaming/)

3. [**Deploy JupyterHub**](./jupyterhub/)

4. [**Deploy NDP Endpoint API**](./ndp-endpoint/)

> **Tip:** Complete each step in order for a smooth deployment experience.

> For MicroK8s clusters needing HTTPS and DNS, see [**`ssl-cert_microk8s`**](./ssl-cert_microk8s/).
