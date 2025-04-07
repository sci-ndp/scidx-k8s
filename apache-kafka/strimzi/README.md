# Apache Kafka Kubernetes Deployment Documentation

This guide provides step-by-step instructions for installing and deleting the Strimzi Operator on a MicroK8s cluster using shell scripts.

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

    Execute the [`install-strimzi-operator.sh`](./install-strimzi-operator.sh) script to deploy the Strimzi Kafka Operator into the `kafka` namespace. The operator will watch for Kafka-related Custom Resources (CRs) and manage the cluster. https://strimzi.io/docs/operators/latest/deploying#assembly-operators-str
    ```bash
    ./install-strimzi-operator.sh
    ```

4. **Deploy a Kafka Cluster**

    Run the [`create-kafka-cluster.sh`](./create-kafka-cluster.sh) script to deploy the Kafka cluster by applying the [`kafka-cluster-0.yaml`](./kafka-cluster-0.yaml) configuration file to your Kubernetes cluster. This file is a Custom Resource (CR) used by the Strimzi Operator to define and manage the Kafka cluster.
    ```bash
    ./apply-kafka-cluster.sh
    ```


5. **Verify the Kafka Cluster**

    


<br><br>
Helm

1. **Add the Strimzi Helm Repository**

    Run the `add-&-update-helm-repo.sh` script to add the Strimzi Helm Chart repository to your helm configuration and update your local helm repository cache to fetch the latest chart versions:
    ```bash
    ./add-&-update-helm-repo.sh
    ```