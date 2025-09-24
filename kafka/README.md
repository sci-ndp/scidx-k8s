# Kafka Kubernetes Deployment Documentation

This guide provides instruction for deploying Strimzi Kafka with TCP Ingress, which walks through:

1. Enabled TCP passthrough for Kafka via **NGINX Ingress Controller**
2. Applied a 4-broker **Strimzi Kafka cluster**
3. Verified the setup using `kcat` over NGINX

## Prerequisites

Ensure you have `kubectl` and `helm` installed and configured to interact with your Kubernetes cluster.

## Additional Resources

For more information on `kubectl` and `helm`, refer to the following resources:

- [kubectl Installation Guide](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Helm Installation Guide](https://helm.sh/docs/intro/install/)
- [Helm Documentation](https://helm.sh/docs/intro/using_helm/)

## Installation

1. **Make Shell Scripts Executable**

    Run the following command to make all the shell scripts executable:

    ```bash
    chmod +x *.sh
    ```

2. **Install the Strimzi Operator**

    The Strimzi Helm workflow lives in [`./strimzi-operator/Makefile`](./strimzi-operator/Makefile). Run the following from the `strimzi-operator` directory to add the Helm repo (idempotent), create the namespace if needed, and install or upgrade the release:

    ```bash
    cd strimzi-operator
    make install
    ```

    `make install` automatically performs `helm repo add`, `helm repo update`, and scopes the operator to the `kafka` namespace via `--set watchNamespaces={kafka}`. 
    
    `make status` inspect the release
    
    `make uninstall` to remove it when you're done experimenting.
    
3. **Upgrade NGINX Ingress Controller with TCP Support**
    
    **Helm-managed ingress:**

    ```bash
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm repo update

    helm upgrade --install nginx-ingress ingress-nginx/ingress-nginx \
        --namespace ingress-nginx --create-namespace \
        --set controller.service.type=LoadBalancer \
        --set tcp.31090="kafka/my-kafka-kafka-0:9094" \
        --set tcp.31091="kafka/my-kafka-kafka-1:9094" \
        --set tcp.31092="kafka/my-kafka-kafka-2:9094" \
        --set tcp.31093="kafka/my-kafka-kafka-3:9094"
    ```

    **MicroK8s ingress add-on:** If the ingress controller was installed with `microk8s enable ingress`, apply the TCP passthrough ConfigMap instead of relying on Helm values:

    ```bash
    ./tcp-passthrough.sh
    ```

    Each TCP rule maps an external port to a specific Kafka broker inside the cluster. NGINX listens on ports `31090–31093` and forwards them to Kafka pods on `9094`.

4. **Deploy a Kafka Cluster**
    
    Update each `listeners.configuration.brokers.broker.advertisedHost` to nginx ingress controller's hostname/external-ip in [`kafka-cluster.yaml`](./kafka-cluster.yaml)

    Run [`install.sh`](./install.sh) script to deploy the Kafka cluster by applying the [`kafka-cluster.yaml`](./kafka-cluster.yaml) configuration file to your Kubernetes cluster. This file is a Custom Resource (CR) used by the Strimzi Operator to define and manage the Kafka cluster.
    ```bash
    ./install.sh
    ```

5. **Verify the Kafka Cluster**

    We confirmed external access to broker 3 using:

    ```bash
    kcat -b 192.168.1.100:31093 -L
    ```

    Output showed:

    - Metadata retrieved from broker 3
    - All brokers registered correctly
    - Topics and partitions accessible
    

    `kcat` (formerly `kafkacat`) is a lightweight command-line tool for producing, consuming, and inspecting Kafka messages.
    Refer to the [kcat documentation](https://github.com/edenhill/kcat).

## Final Result

- ✅ Strimzi Kafka with 4 brokers
- ✅ NGINX Ingress with TCP passthrough to each broker
- ✅ One broker (broker 3) correctly pinned to an internal MicroK8s node
- ✅ Verified with `kcat` over public IP + custom port
