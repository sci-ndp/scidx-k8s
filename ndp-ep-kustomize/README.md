# NDP Endpoint – Kustomize

Lightweight Kustomize overlays for deploying the National Data Platform Endpoint (NDP-EP) API across `dev`, `test`, and `prod` environments.

## Prerequisites
- `kubectl` 1.21 or newer (includes `kubectl apply -k` support)
- Access to the target cluster/context with permission to create namespaces, secrets, and workloads

## Layout
- `kustomize/base`: shared manifests (deployment, service, ingress)
- `kustomize/overlays/<env>`: environment-specific namespace plus secret generator

## Configure Secrets
1. Change into the overlay directory you plan to deploy, e.g. `kustomize/overlays/dev`.
2. Copy the template and populate it with real values:
   ```bash
   cp ndp-ep-env-secret.env.template ndp-ep-env-secret.env
   ```
3. Fill out `ndp-ep-env-secret.env`. The file stays local (ignored by Git) and is converted into a Kubernetes secret at deploy time.

## Dry Run (optional)
- Render manifests locally:
  ```bash
  kubectl kustomize kustomize/overlays/<env>
  ```
- Compare against the cluster without applying changes:
  ```bash
  kubectl apply --dry-run=server -k kustomize/overlays/<env>
  ```

## Deploy
Namespaces are managed per overlay (`ndp-ep-dev`, `ndp-ep-test`, `ndp-endpoint`).

```bash
kubectl apply -k kustomize/overlays/dev
kubectl apply -k kustomize/overlays/test
kubectl apply -k kustomize/overlays/prod
```

Kustomize creates the namespace (if needed), builds the secret from your `.env`, and applies the shared resources.

## Cleanup
Remove everything defined in an overlay:

```bash
kubectl delete -k kustomize/overlays/<env>
```
