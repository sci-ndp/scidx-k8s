# Kafka on Kubernetes (Strimzi)

Use this repo to deploy a 4-broker Strimzi Kafka cluster and expose it via NGINX TCP passthrough. Make targets handle the install, ingress wiring, and broker advertisedHost patching for you.

## Prereqs

- `kubectl` and `helm` installed and able to reach your cluster.
- `kcat` if you want to run the verification target.

## Installation

1. Copy and edit the example once so all targets share the same settings:

    ```bash
    cp config.mk.example config.mk
    ```

    >`KUBE_CONTEXT` defaults to your current kubectl context (or `microk8s` if none); override in `config.mk` as needed.

    Key settings in `config.mk`:
    - `KUBE_CONTEXT`: kube context to target (overrides current).
    - `BROKER_HOST`: external hostname used for advertisedHost and kcat verification.
    
    Others:
    - `NAMESPACE`: namespace for operator and Kafka cluster.
    - `RELEASE_NAME`, `CHART`, `CHART_VERSION`, `HELM_REPO_NAME`, `HELM_REPO_URL`: Helm release/chart/repo details for the Strimzi operator.

2. Install/upgrade the Strimzi operator in the target namespace:
    ```bash
    make install-operator
    ```

3. Patch advertisedHost in kafka-cluster.yaml with BROKER_HOST and apply the cluster
    ```bash
    make install
    ```

## Expose via NGINX TCP

Choose one path:

- Helm-managed ingress-nginx:
  ```bash
  make tcp-passthrough-helm
  ```
- MicroK8s ingress addon:
  ```bash
  make tcp-passthrough-microk8s
  ```

## Verify

Fetch metadata from the broker endpoint:

```bash
make verify
```

## Cleanup

```bash
make uninstall           # remove kafka-cluster.yaml resources
make uninstall-operator  # remove Strimzi operator
```
