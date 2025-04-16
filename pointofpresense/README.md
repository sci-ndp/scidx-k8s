# National Data Platform Endpoint(formerly POP) Kubernetes Deployment Documentation

This guide provides step-by-step instructions for installing and deleting the Strimzi Operator on a MicroK8s cluster using shell scripts.

## Prerequisites
Ensure you have `kubectl` and `helm` installed and configured to interact with your Kubernetes cluster.

## Additional Resources

For more information on `kubectl` and `helm`, refer to the following resources:

- [kubectl Installation Guide](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

## Installation
1. **Make Shell Scripts Executable**

    Run the following command to make all the shell scripts executable:
    ```bash
    chmod +x *.sh
    ```
2. **Configuring Environment Variables**
      
      Copy the template to create your Secret file:
      ```bash
      ./copy-secret.sh
      ```
      
3. **Edit the values in `stringData` in `pop-env-secret.yaml`(created by pop-env-secret.yaml) to match your environment.**

### Deploy NDP Endpoint (formerly POP)

1. Apply all the other manifests with 'pop' prefix
   ```bash
   ./apply.sh
