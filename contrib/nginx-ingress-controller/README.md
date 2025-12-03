# NGINX Ingress Controller Installation Guide Documentation

This guide provides step-by-step instructions for installing and deleting the NGINX Ingress Controller on an EKS cluster or a MicroK8s cluster using shell scripts. For more detailed information, refer to the [NGINX Ingress Controller documentation](https://kubernetes.github.io/ingress-nginx/).


## Prerequisites
Ensure you have `kubectl` and `helm` installed and configured to interact with your Kubernetes cluster.


## Additional Resources
For more information on `kubectl` and `helm`, refer to the following resources:
- [kubectl Installation Guide](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Helm Installation Guide](https://helm.sh/docs/intro/install/)
- [Helm Documentation](https://helm.sh/docs/intro/using_helm/)


## Installation

#### For AWS EKS Cluster

1. **Make Shell Scripts Executable**

    Run the following command to make all the shell scripts executable:
    ```bash
    chmod +x *.sh
    ```

2. **Add the NGINX Ingress Helm Repository**

    Run the `add-&-update-helm-repo.sh` script to add the NGINX Ingress Helm repository and update it:
    ```bash
    ./update-helm-repo.sh
    ```

3. **Install the NGINX Ingress Controller**

    Execute the `install.sh` script to install the NGINX Ingress Controller with a LoadBalancer service type:
    ```bash
    ./install.sh
    ```

4. **Verify the Installation**

    Use the `verify-installation.sh` script to ensure the ingress controller pods are running and to check the service's external IP:
    ```bash
    ./verify-installation.sh
    ```

#### For MicroK8s Cluster

1. **Enable MetalLB**

    MetalLB is a load-balancer implementation for bare metal Kubernetes clusters, providing the functionality of a cloud provider's load balancer. 
    
    Run the following command to enable MetalLB, which provides load balancer functionality:
    ```bash
    microk8s enable metallb
    ```

2. **Make Shell Scripts Executable**

    Run the following command to make all the shell scripts executable:
    ```bash
    chmod +x *.sh
    ```

3. **Add the NGINX Ingress Helm Repository**

    Run the `add-repo.sh` script to add the NGINX Ingress Helm repository and update it:
    ```bash
    ./add-&-update-repo.sh
    ```

4. **Install the NGINX Ingress Controller**

    Execute the `install.sh` script to install the NGINX Ingress Controller with a LoadBalancer service type:
    ```bash
    ./install.sh
    ```

5. **Verify the Installation**

    Use the `verify-installation.sh` script to ensure the ingress controller pods are running and to check the service's external IP:
    ```bash
    ./verify-installation.sh
    ```

## Deletion

1. **Uninstall the NGINX Ingress Controller**

    Run the `delete.sh` script to uninstall the NGINX Ingress Controller and delete the `ingress-nginx` namespace:
    ```bash
    ./delete.sh
    ```

2. **Verify the Deletion**

    Execute the `verify-deletion.sh` script to confirm that all resources in the `ingress-nginx` namespace have been removed:
    ```bash
    ./verify-deletion.sh
    ```

By following these steps, you can manage the lifecycle of the NGINX Ingress Controller on your EKS or MicroK8s cluster.
