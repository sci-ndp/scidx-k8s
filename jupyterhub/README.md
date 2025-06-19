# NDP Jupyterhub Kubernetes Deployment Notes


## jupyterhub-secret
Keycloak client's credentials are passed as k8s secret for hub server to read from.
```sh
kubectl create secret generic jupyterhub-secret --from-file=values.yaml=jupyterhub_secret.yaml -n jupyterhub
```
--from-file=values.yaml=jupyterhub_secret.yaml:
Loads the contents of jupyterhub_secret.yaml and stores it in the secret under the key values.yaml.<br>
Result secret will look like this:
```yaml
  apiVersion: v1
  kind: Secret
  metadata:
    name: jupyterhub-secret
  data:
    values.yaml: <base64-encoded contents of jupyterhub_secret.yaml>
```


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