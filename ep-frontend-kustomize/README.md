# NDP EP Frontend – Kustomize

Lightweight Kustomize overlays for deploying the National Data Platform Endpoint (NDP-EP) frontend console across `dev`, `test` (added later), and `prod` (added later) environments.

## Prerequisites
- `kubectl` 1.21 or newer (includes `kubectl apply -k` support)
- Access to the target cluster/context with permission to create namespaces, secrets, and workloads

## Layout
- `kustomize/base`: shared manifests (deployment, service, ingress)
- `kustomize/overlays/<env>`: environment-specific namespace plus secret generator

## Configure Overlay (Ingress + Secrets)
1. Change into the overlay you plan to deploy:
   ```bash
   cd kustomize/overlays/prod   # or kustomize/overlays/(dev|test)
   ```
2. Set the public hostname in `ingress-patch.yaml` (replace `value: ndp-dev-xxx.chpc.utah.edu` with your ingress controller's DNS name).
   > Note: Default ingress path is `/`, so your ndp endpoint admin console will be served at `your-hostname/`.
3. Edit the `NDP_EP_API_URL` value in **`kustomization.yaml`** (`configMapGenerator`) to point to your deployed NDP Endpoint API (e.g., `https://ndp-dev-xxx.chpc.utah.edu/api`). To ensure the frontend console can connect to correct the backend API to monitoring it.


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
Namespaces are managed per overlay (`ndp-ep-frontend-dev`, `ndp-ep-frontend-test`, `ndp-ep-frontend`).

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

## Next Steps
Go back to [**SciDx Kubernetes Document**](https://github.com/sci-ndp/scidx-k8s?tab=readme-ov-file#deploy-ndp-endpoint-admin-console) for more details about the overall Kubernetes setup for SciDx service.
