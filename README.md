# sciDX Kubernetes Resource

This repository contains Kubernetes manifests and supporting files for deploying and managing scidx services stack within a Kubernetes cluster.

## Prerequisite - External Access Setup

To ensure an error-free deployment and make the ingress resources work correctly, you need to install the ingress controller first. Follow the steps below to set up external access for both the `pointofpresense` and `staging` deployments in your Kubernetes cluster:

1. **Install the Ingress Controller**:
    Navigate to the [`./nginx-ingress-controller`](./nginx-ingress-controller/) directory and follow the provided instructions to install the NGINX Ingress Controller in your cluster.
2. **Deploy `pointofpresence` or `staging`**:
    Once the ingress controller is installed, navigate to either the [`./pointofpresense`](./pointofpresense) or [`./staging`](./staging) directory and follow the deployment instructions to deploy the respective applications.

By following to these, you will ensure that both `pointofpresense` and `staging` deployments are accessible externally.
