# Test Overlay Deployment (ndp-ep-test)

Notes for applying the `kustomize/overlays/test` overlay to the test cluster.

## Prepare secrets and config
1) API env vars: copy `ndp-ep-env-secret.env.template` to `ndp-ep-env-secret.env` and fill in the values required for the test environment. The file is consumed by `secretGenerator` to create `ndp-ep-env-secret`.
2) Runtime kubeconfig for the app: place the kubeconfig the app should use at `./kubeconfig/config-202`. It is packaged into the `ndp-ep-kubeconfig` secret and mounted into the container at `/code/yutian/.kubeconfig` (see `kubeconfig-patch.yaml`). Keep this file private and out of version control.

## Deploy
```bash
cd /Users/yutian1/dev/sci/kube/scidx-k8s-dev/ndp-ep-kustomize
kubectl apply -k kustomize/overlays/test
```
This creates/updates the `ndp-ep-test` namespace, deploys `ndp-ep-api` with image `yutianqin/ndpep:v1`, applies the ingress host `ndp-test-211.chpc.utah.edu`, and configures the HPA and kubeconfig mount.

## Verify
- Check rollout: `kubectl -n ndp-ep-test get deploy,pods`
- Confirm ingress and host: `kubectl -n ndp-ep-test get ingress`
- If the app needs cluster access, exec into the pod and verify `/code/yutian/.kubeconfig` is present.

## Updating image or host
- Image tag/name is set in `kustomization.yaml` under `images:`.
- Ingress host is patched in `ingress-patch.yaml`; update it if the test hostname changes.
