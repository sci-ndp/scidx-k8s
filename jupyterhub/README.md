# NDP Jupyterhub Kubernetes Deployment Doumentation

## Prerequisites

Ensure you have `kubectl` and `helm` installed and configured to interact with your Kubernetes cluster.

Nginx ingress controller is installed on your cluster; if not, you can follow [installation guide](../nginx-ingress-controller/README.md).

## Additional Resources

For more information on `kubectl` and `helm`, refer to the following resources:

- [kubectl Installation Guide](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Helm Installation Guide](https://helm.sh/docs/intro/install/)
- [Helm Documentation](https://helm.sh/docs/intro/using_helm/)

## Creating the JupyterHub Secret

To provide Keycloak client credentials to JupyterHub, in [`./helm/jupyterhub_secret.yaml`](./helm/jupyterhub_secret.yaml), insert the `client_id` and `client_secret` values obtained from NDP admins


## Deploying NDP JupyterHub on Kubernetes Cluster

There is a Makefile provided to simplify the deployment and management of JupyterHub on your Kubernetes cluster using Helm.

### Deployment Prerequisites

Ensure that jupyterhub_secret.yaml  contains the correct Keycloak client credentials.

### Common Tasks

1. **Update Helm Chart Dependencies:** Fetch and update Helm chart dependencies listed in `Chart.yaml`.

   ```bash
   make update-dependency
   ```

2. **Generate Configuration:** This step creates a `config.yaml` file by embedding the contents of `spawner.py` into the `values.yaml` file.

   ```bash
   make generate
   ```

3. **Create JupyterHub Secret:** Store Keycloak client credentials as a Kubernetes secret:

   ```bash
   make create-jupyterhub-secret
   ```

4. **Deploy JupyterHub**
   Deploy or upgrade JupyterHub using Helm:

   ```bash
   make deploy
   ```

5. **Check Deployment Status**

   ```bash
   make status
   ```

6. **Get Ingress Details**
   Retrieve the Ingress IP or hostname for accessing JupyterHub:

   ```bash
   make get-ingress
   ```

7. **Uninstall JupyterHub**
   Remove the JupyterHub deployment:

   ```bash
   make uninstall
   ```

8. **Clean Up Generated config.yaml File**

   ```bash
   make clean
   ```

### Notes

- You may need to adjust variables in the Makefile (such as `NAMESPACE` or `VALUES_FILE`) to match your setup.
- For troubleshooting, check the output of each command and consult your Kubernetes cluster logs as needed.

## JupyterHub Secret Explaination

By executing `make create-jupyterhub-secret`, you basically run:
```sh
kubectl create secret generic jupyterhub-secret \
  --from-file=values.yaml=jupyterhub_secret.yaml \
  -n jupyterhub
```

- The `--from-file=values.yaml=jupyterhub_secret.yaml` flag loads the contents of `jupyterhub_secret.yaml` into the secret under the key `values.yaml`.
- The resulting secret will look like:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: jupyterhub-secret
data:
  values.yaml: <base64-encoded contents of jupyterhub_secret.yaml>
```