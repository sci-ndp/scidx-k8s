# Kafka on Kubernetes (Strimzi)

Use this repo to deploy a 4-broker Strimzi Kafka cluster and expose it via NGINX TCP passthrough. Make targets handle the install, ingress wiring, and broker advertisedHost patching for you.

## Prerequisites

- `kubectl` and `helm` installed and able to reach your cluster.
- `kcat` if you want to run the verification target.

## **Installation**

1. #### **Copy default make config**, all make targets share the same settings

    ```bash
    cp config.mk.example config.mk
    ```

    Then open ./config.mk and set values<br>
    ```bash
    vi config.mk
    ```
    Key one: **`BROKER_HOST`** (required): external DNS.

    [Other settings in `config.mk`](#configmk-settings) can be changed as needed.
    

2. #### **Install/upgrade the Strimzi operator** in the target namespace
    ```bash
    make install-operator
    ```

3. #### **Deploy Kafka cluster:** patch advertisedHost in kafka-cluster.yaml with BROKER_HOST and apply it
    ```bash
    make install
    ```

## **Expose** via NGINX TCP Passthrough

Choose one path:

- Helm-managed ingress-nginx:
  ```bash
  make tcp-passthrough-helm
  ```
- MicroK8s ingress addon:
  ```bash
  make tcp-passthrough-microk8s
  ```

## **Optional follow-up**: verify and cleanup

Verify broker endpoint metadata (uses `kcat`):
> Requires `kcat` installed;<br>
> Wait until deployment for brokers is ready. Check kafka cluster status, run `kubectl get pods -n ckan -w`.
```bash
make verify
```

Cleanup:<br>
`make uninstall` removes the deployed Kafka cluster resources.<br>
`make uninstall-operator` removes the Strimzi operator release.


## Next Steps
Go back to [**SciDx Kubernetes Document**](https://github.com/sci-ndp/scidx-k8s?tab=readme-ov-file#deploy-kafka-strimzi) for more details about the overall Kubernetes setup for SciDx service.

<br>

## config.mk Settings
**`BROKER_HOST`(required)**: external DNS name that clients use to reach Kafka brokers, installation will fail without it.

`KUBE_CONTEXT`: kubernetes cluster context (defaults to **kubectl config current-context** if leaves empty, or **"microk8s"** if none).

`NAMESPACE`: namespace to deploy operator and Kafka cluster into (default: **kafka**).

`RELEASE_NAME`, `CHART`, `CHART_VERSION`, `HELM_REPO_NAME`, `HELM_REPO_URL`: Helm release/chart/repo details for the Strimzi operator with default values.

Example, replace every <...>:
```mk
# Strimzi operator settings
# ------------------------------
# Namespace for operator and cluster
NAMESPACE = kafka
# Helm release name for the operator
RELEASE_NAME = strimzi
# Strimzi chart version
CHART_VERSION = 0.45.0
# Chart reference
STRIMZI_CHART = strimzi/strimzi-kafka-operator
# Helm repo name
HELM_REPO_NAME = strimzi
# Helm repo URL
HELM_REPO_URL = https://strimzi.io/charts


# Kafka broker connection
# ------------------------------
# External hostname used for advertisedHost and kcat
BROKER_HOST = <kafka.example.com>


# Kubernetes context
# ------------------------------
# kubectl/helm context to target (overrides current)
KUBE_CONTEXT = <arn:aws:eks:us-west-2:xxxxxxxxxxxx:cluster/cluster-name>
```
[Back to `Installation`](#copy-default-make-config-all-make-targets-share-the-same-settings)