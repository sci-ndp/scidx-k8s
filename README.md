# ndp-k8s-resource

This repository contains Kubernetes manifests and supporting files for deploying and managing applications within a Kubernetes cluster.

## Prerequisite - External Access Setup

To ensure an error-free deployment and make the ingress resources work correctly, you need to install the ingress controller first. Follow the steps below to set up external access for both the `pop` and `dspaces` deployments in your Kubernetes cluster:

1. **Install the Ingress Controller**:
    Navigate to the [`./ingress-controller`](./ingress-controller/) directory and follow the provided instructions to install the NGINX Ingress Controller in your cluster.
2. **Deploy `pop` or `dspaces`**:
    Once the ingress controller is installed, navigate to either the [`./pop`](./pop) or [`./dspaces`](./dspaces) directory and follow the deployment instructions to deploy the respective applications.

By following to these, you will ensure that both `pop` and `dspaces` deployments are accessible externally.
