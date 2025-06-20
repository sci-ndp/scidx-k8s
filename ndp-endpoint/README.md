# National Data Platform Endpoint(formerly POP) Kubernetes Deployment Documentation

This guide provides step-by-step instructions for installing and deleting the Strimzi Operator on a MicroK8s cluster using shell scripts.

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

2. **Configuring Environment Variables**

    Copy the template to create your Secret file:

    ```bash
    ./copy-secret.sh
    ```

3. **Edit the values in `stringData` in `pop-env-secret.yaml` to match your environment.**

    If you have deployed Kafka, configure the Kafka connection settings by specifying the external IP of the NGINX ingress controller as `KAFKA_HOST` and choose one of the following ports: `31090`, `31091`, `31092`, or `31093` for `KAFKA_PORT`.

    ```yaml
    KAFKA_CONNECTION: "True"    # Set to "True" to enable Kafka connectivity
    KAFKA_HOST: ""              # Enter the Kafka broker's hostname or IP address
    KAFKA_PORT: ""              # Enter the Kafka broker's port number
    ```

4. **Configure ingress**:

    Option 1: Use a DNS name with HTTPS

    If you have configured a DNS name with HTTPS support for the NGINX ingress controller, update the host in the  file. By default, it is set to vdc-190.chpc.utah.edu. Modify the spec.tls.hosts and spec.rules.host fields to match your domain, for example:

    ```yaml
    spec:
        ingressClassName: nginx
        tls:
            - hosts:
                - your-domain.example.com
            secretName: pop-api-tls
        rules:
            - host: your-domain.example.com
            http:
                paths:
                - path: /pop(/|$)(.*)
                    pathType: ImplementationSpecific
                    backend:
                    service:
                        name: pop-api-service
                        port:
                        number: 8003
    ```

    Option 2: No DNS name configured

    If you do not have a DNS name configured for the ingress controller, use the  file instead. This file provides a basic ingress configuration without a specific host:

    ```yaml
    spec:
        ingressClassName: nginx
        rules:
            - http:
                paths:
                - path: /pop(/|$)(.*)
                    pathType: ImplementationSpecific
                    backend:
                    service:
                        name: pop-api-service
                        port:
                        number: 8001
    ```

    > To use this file, replace the default pop-ingress.yaml with template-ingress.yaml. First, back up or remove the existing pop-ingress.yaml, then rename template-ingress.yaml to pop-ingress.yaml so it is applied by the deployment script:

    ```bash
    # Back up the default pop-ingress.yaml (optional)
    mv pop-ingress.yaml pop-ingress.yaml.bak

    # Rename template-ingress.yaml to pop-ingress.yaml
    mv template-ingress.yaml pop-ingress.yaml
    ```

### Deploy NDP Endpoint (formerly POP)

1. Apply all the other manifests with 'pop' prefix

    ```bash
    ./apply.sh
    ```

   The `apply.sh` script will:

    * Apply the namespace (`pop-namespace.yaml`).
    * Apply the environment secrets (`pop-env-secret.yaml`).
    * Apply all other manifests with the pop prefix, including `pop-ingress.yaml`, `pop-deployment.yaml`, `pop-service.yaml`, etc.
