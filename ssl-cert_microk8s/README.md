# Documentation: Adding a Certificate using cert-manager addon in MicroK8s

This documentation shows you how to add a certificate by using the cert-manager addon of MicroK8s. The cert-manager is a native Kubernetes certificate management controller that helps with issuing and renewing certificates from various sources, such as Let's Encrypt, HashiCorp Vault, and self-signed certificates.
For more information, refer to the [MicroK8s documentation on cert-manager](https://microk8s.io/docs/addon-cert-manager).

> **Note:** Let's Encrypt certificates last 90 days, but cert-manager automatically renews them 30 days before expiry.

### Prerequisites
Ensure that your domain resolves to the external IP of your NGINX Ingress controller's load balancer service.

### Steps

1. **Verify NGINX Ingress Controller Installation:**
    ```sh
    kubectl get svc -n ingress-nginx
    ```
    If the NGINX Ingress controller is not installed, navigate to the [`../nginx-ingress-controller`](../nginx-ingress-controller) directory and follow the instructions to install the NGINX Ingress controller.

2. **Enable cert-manager Addon**: Enable the cert-manager addon in your MicroK8s cluster.
    ```sh
    microk8s enable cert-manager
    ```

3. **Create ClusterIssuer**: Define an ClusterIssuer resource to specify the certificate authority.
    ```sh
    kubectl apply -f letsencrypt_cluster_issuer.yaml
    ```

### Verify
1. **Verify Cluster Issuer Status:**
    ```sh
    kubectl get clusterissuer letsencrypt-prod -o yaml
    ```

2. **Apply Example Ingress for dspaces (if deployed):**
    ```sh
    kubectl apply -f example_dspaces_ingress.yaml
    ```
    At this point, cert-manager will automatically request a certificate from Let's Encrypt and store it in a Kubernetes Secret named `dspaces-tls`.

3. **Verify Certificate:**
    ```sh
    kubectl get certificate -n dspaces
    kubectl get secret -n dspaces dspaces-tls
    ```


<br>


## Optional
Relavant code is inside [`./archive`](./archive)

If you have existing credentials: you can follow what's below:
To package the provided credentials (`fullchain.pem` and `privkey.pem`) into a Kubernetes Secret and reference them in the Ingress with the host field, follow these steps:

### Steps

1. **Create the Kubernetes Secret:**

    ```sh
    kubectl create secret tls my-ssl-cert \
        --cert=fullchain.pem \
        --key=privkey.pem
    ```

2. **Reference the Secret in the Ingress Resource:**

    ```yaml
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: example-ingress
      namespace: default
    spec:
      tls:
      - hosts:
         - your-domain.com
         secretName: my-ssl-cert
      rules:
      - host: your-domain.com
         http:
            paths:
            - path: /
              pathType: Prefix
              backend:
                 service:
                    name: your-service
                    port:
                      number: 80
    ```

Replace `your-domain.com` with your actual domain and `your-service` with the name of your service.
