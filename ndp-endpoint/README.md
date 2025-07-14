# National Data Platform Endpoint(formerly POP) Kubernetes Deployment Documentation

This guide provides step-by-step instructions for installing and deleting the Strimzi Operator on a MicroK8s cluster using shell scripts.

## Prerequisites

Ensure you have `kubectl` and `helm` installed and configured to interact with your Kubernetes cluster.

## Additional Resources

For more information on `kubectl` and `helm`, refer to the following resources:

- [kubectl Installation Guide](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

## Configuration

1. **Make Shell Scripts Executable**

    Run the following command to make all the shell scripts executable:

    ```bash
    chmod +x *.sh
    ```

2. **Configuring Environment Variables**

    Copy the template to create your Secret file:

    ```bash
    cp secret-template.yaml pop-env-secret.yaml
    ```

3. **Edit the values in `stringData` in pop-env-secret.yaml to match your environment.**

    If you have deployed Kafka Cluster, configure the Kafka connection settings by specifying the external IP of the NGINX ingress controller as KAFKA_HOST and choose one of the following ports: `31090`, `31091`, `31092`, or `31093` for KAFKA_PORT.

    ```yaml
    KAFKA_CONNECTION: "True"    # Set to "True" to enable Kafka connectivity
    KAFKA_HOST: ""              # Enter the Kafka broker's hostname or IP address
    KAFKA_PORT: ""              # Enter the Kafka broker's port number
    ```

4. **Configure ingress**:
    
    If no DNS name is configured for the Nginx ingress controller, skip this step. 
    
    > By default, we apply the already defined pop-ingress.yaml. This file provides a basic ingress configuration without a specific host

    Optional: 

    If you have configured a DNS name with HTTPS support for the Nginx ingress controller, update pop-ingress.yaml accordingly. Here is an example:

    ```yaml
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
    name: pop-ingress
    namespace: pop
    annotations:
        nginx.ingress.kubernetes.io/rewrite-target: /$2
        cert-manager.io/cluster-issuer: "letsencrypt-prod"
    spec:
    ingressClassName: nginx
    tls:
        - hosts:
            - vdc-190.chpc.utah.edu
        secretName: pop-api-tls
    rules:
        - host: vdc-190.chpc.utah.edu
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

## Deploy NDP Endpoint

To deploy all required resources, run the following script:

```bash
./apply.sh
```

The apply.sh script will:
- Apply the `pop-namespace.yaml` to create the namespace.
- Wait for the `pop` namespace to be ready.
- Apply `pop-env-secret.yaml` (script exits with an error if missing).
- Apply all other `pop-*.yaml` manifests except the namespace and secret files.

You will see progress messages for each step. When the script completes, all manifests will be applied to your cluster.
