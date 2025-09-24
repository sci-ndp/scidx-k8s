# Dataspaces EKS Deployment Documentation

This document provides a overview of the Kubernetes manifests located in the current `dspaces` directory. These manifests are used to deploy and manage the Dataspaces API and Dataspaces Server in a EKS cluster.

## Prerequisites

Before deploying the resources, ensure you have the following prerequisites:

- A running EKS cluster.
- `kubectl` configured to interact with your EKS cluster.
- Necessary permissions to create resources in the cluster.

## Additional Resources

For more information on Kubernetes and EKS, refer to the following resources:

- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Amazon EKS Documentation](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

## Table of Contents
1. [Introduction](#introduction)
2. [Manifests Overview](#manifests-overview)
3. [Deployment Instructions](#deployment-instructions)
    - [Automatic Deployment (Recommended)](#1-automatic-deployment-recommended)
    - [Manual Deployment (Step-by-Step)](#2-manual-deployment-step-by-step)
    - [Verifying the Deployment](#3-verifying-the-deployment)
    - [Next Steps](#4-next-steps)
4. [Troubleshooting](#troubleshooting)
5. [Feedback](#feedback)

## Introduction

This directory contains Kubernetes manifests that define the desired state of various resources within a Kubernetes cluster. These manifests include configurations for namespaces, deployments, services, config maps, secrets, and ingress resources.

## Manifests Overview

The following is a list of the Kubernetes manifests available in this directory:

Dataspaces API
- `api-deployment.yaml`: Defines the deployment for the Dataspaces API.
- `api-service.yaml`: Defines the service for the Dataspaces API. 
- `dspaces-rbac.yaml`: Role and RoleBinding for accessing services and endpoints.

Dataspaces Server
- `dspaces-deployment.yaml`: Defines the deployment for the Dataspaces Server.
- `dspaces-service.yaml`: Defines the service for the Dataspaces Server.
- `dspaces-configmap.yaml`: ConfigMap for the Dataspaces Server configuration.

General
- `dspaces-namespace.yaml`: Defines the namespace for the all Dataspaces resources.
- `ingress.yaml`: Defines the ingress resource for external access to the Dataspaces API.

## Deployment Instructions

You have two ways to deploy the Dataspaces API and Dataspaces Server: 

1. **Automatic Deployment** (Recommended) - Using `apply-k8s-rsc.sh` to apply all Kubernetes resources at once.
2. **Manual Deployment** - Applying each resource step-by-step for better control and debugging.

### 1. Automatic Deployment (Recommended)

For a quick deployment, run the provided script:

```sh
chmod +x apply-k8s-rsc.sh
./apply-k8s-rsc.sh
```
This script will:
* Apply the namespace first.
* Wait until the namespace is fully available.
* Apply all other Kubernetes resources in the directory.

### 2. Manual Deployment (Step-by-Step)
If you prefer a more controlled approach, apply each resource in sequence:

- **Create the Namespace (Required before deploying other resources)**
    ```sh
    kubectl apply -f dspaces-namespace.yaml
    ```

- **Apply the ConfigMap**
    ```sh
    kubectl apply -f dspaces-configmap.yaml
    ```

- **Deploy the Dataspaces API**
    ```sh
    kubectl apply -f api-deployment.yaml
    kubectl apply -f api-service.yaml
    ```

- **Deploy the Dataspaces Server**
    ```sh
    kubectl apply -f dspaces-deployment.yaml
    kubectl apply -f dspaces-service.yaml
    ```

- **Apply Role-Based Access Control (RBAC)**
    ```sh
    kubectl apply -f dspaces-rbac.yaml
    ```

- **Set Up Ingress (For External Access)**
    ```sh
    kubectl apply -f ingress.yaml
    ```

### 3. Verifying the Deployment
After deployment, confirm everything is running as expected:

Verify the deployment status with the following commands:

- **Check Pod Status**:
    ```sh
    kubectl get pods -n dspaces
    ```

- **Check Services Status**:
    ```sh
    kubectl get svc -n dspaces
    ```

To access the deployment using the ingress external IP, follow these steps:

1. **Get the External IP of the Ingress**:
    ```sh
    kubectl get ingress -n dspaces
    ```
    Look for the `ADDRESS` field in the output, which contains the external IP.

2. **Access the Services**:
    Open a web browser and navigate to the external IP address obtained in the previous step. You should be able to access the Dataspaces API and Server through the configured ingress routes.

For example, if the external IP is `203.0.113.0`, you can access the services at:
- `http://203.0.113.0/dsapces`


### 4. Next Steps
Once deployed, you can access the Dataspaces API and Server through the configured ingress. If needed, delete the deployment using:
```sh
chmod +x delete-k8s-rsc.sh
./delete-k8s-rsc.sh
```
This will clean up all resources that were deployed.

## Troubleshooting

If you encounter any issues during the deployment, you can use the following commands to troubleshoot:

- **View Pod Logs**:
    ```sh
    kubectl logs <pod-name> -n dspaces
    ```

- **Describe Resource**:
    ```sh
    kubectl describe <resource-type> <resource-name> -n dspaces
    ```
    For example, to describe a pod:
    ```sh
    kubectl describe pod my-pod -n dspaces
    ```

## Feedback

If you have any feedback or suggestions for improving this documentation, please open an issue or submit a pull request in the repository.
