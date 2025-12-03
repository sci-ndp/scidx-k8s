# SciDX Kubernetes Resources
Deployable configs for the SciDX services stack on Kubernetes: JupyterHub, CKAN, Kafka, and the NDP Endpoint API plus admin console. Core components live at the repo root; optional helpers are put under `contrib/`.

## Components at a glance
| Component | Location | Notes |
| --- | --- | --- |
| JupyterHub | `ndp-jupyterhub/` (submodule) | Helm config and docs with Makefile |
| CKAN | `ckan-helm/` (submodule) | Helm chart fork with Makefile |
| Kafka | `kafka/` | Strimzi provisioned Kafka cluster with Makefile |
| NDP Endpoint API | `ep-api-kustomize/` | Kustomize overlays |
| NDP Endpoint Admin Console | `ep-frontend-kustomize/` | Kustomize overlays |
| Optional helpers | `contrib/` | non-core helpers |

## Prerequisites
- `kubectl` 1.21+ against a cluster/context where you can create namespaces, ingresses, and PVCs.
- Helm 3, kustomize support (built into recent kubectl), and `make`.
- Git with SSH access to GitHub if you use the `git@` submodule URLs; switch `.gitmodules` to HTTPS if needed.

## Clone this repo
```bash
git clone --recurse-submodules https://github.com/sci-ndp/scidx-k8s.git

cd scidx-k8s
```
>If you already cloned without submodules
```git submodule update --init --recursive```

## Installation
1) Confirm cluster context availability:
   ```bash
   kubectl config current-context
   ```
   >Optional: install ingress-nginx controller if your cluster lacks an ingress controller, see [contrib/nginx-ingress-controller](contrib/nginx-ingress-controller/)
2) #### Deploy Kafka (Strimzi):
   ```bash
   cd kafka
   ```
   and follow [**Kafka Deployment Document**](./kafka/README.md); by following, what you will do:
   ```bash
   cp config.mk.example config.mk   
   # And edit config.mk to set BROKER_HOST and KUBE_CONTEXT
   make install-operator
   make install
   # Optional: make tcp-passthrough-helm   # expose via ingress-nginx
   # Optional: make verify
   ```
3) #### Deploy CKAN:
   ```bash
   cd ckan-helm
   ```
   and follow [**CKAN Deployment Document**](https://github.com/sci-ndp/ckan-helm/blob/master/README.md); by following, what you will do:
   ```bash
   cp config.example.mk config.mk
   # edit config.mk to set KUBE_CONTEXT
   cp site-values.example.yaml site-values.yaml   
   # edit site-values.yaml to setsite URL, ingress host, admin creds
   make update
   make deploy
   ```
4) #### Deploy JupyterHub:
   ```bash
   cd ndp-jupyterhub/helm-generic
   # temp switch to central-var branch, will merge into main later
   git fetch origin
   git switch central-var
   ```
   and follow [**generic NDP JupyterHub Deployment Document**](https://github.com/national-data-platform/ndp-jupyterhub/blob/central-var/helm-generic/README.md); by following, what you will do:
   ```bash
   # consult ndp admin for secrets values per ndp-jupyterhub/README.md
   # common flow: helm repo add/update, set secret for auth client, create jupyterhub-secret, site-values.yaml override, then:
   make deploy
   ```
5) #### Deploy NDP Endpoint API:
   ```bash
   cd ep-api-kustomize
   ```
   and follow [**NDP Endpoint API Deployment Document**](./ep-api-kustomize/README.md); by following, what you will do:
    ```bash
   cd <overlay(prod|dev|test)>
   cp ndp-ep-env-secret.env.template ndp-ep-env-secret.env
   # edit ndp-ep-env-secret.env to fill in secrets
   kubectl apply -k kustomize/overlays/prod   # or dev/test
   ```
6) #### Deploy NDP Endpoint Admin Console:
   ```bash
   cd ep-frontend-kustomize
   ```
   and follow [**NDP Endpoint Admin Console Deployment Document**](./ep-frontend-kustomize/README.md); by following, what you will do:
   ```bash
   cd <overlay(prod|dev|test)>
   # edit NDP_EP_API_URL to point to deployed NDP Endpoint API
   kubectl apply -k kustomize/overlays/prod   # or dev/test
   ```
