# SciDX Kubernetes Resources

This repository provides Kubernetes manifests and supporting files for deploying and managing the SciDX services stack.

## Deployment

Follow these steps to deploy SciDX software stack on Kubernetes cluster:

1. [**Install the NGINX Ingress Controller**](./nginx-ingress-controller/)
    
2. [**Deploy CKAN**](https://github.com/sci-ndp/ckan-helm)

3. [**Deploy Kafka Cluster**](./kafka/)

4. [**Deploy NDP JupyterHub**](https://github.com/sci-ndp/jhub-helm)

5. [**Deploy NDP Endpoint API**](./ndp-ep/)

> **Tip:** Complete each step in order for a smooth deployment experience.

> For MicroK8s clusters needing HTTPS and DNS, see [**`ssl-cert_microk8s`**](./ssl-cert_microk8s/).
