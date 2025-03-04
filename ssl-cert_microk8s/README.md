# Install certificate

If you don't have certificate credentials, you can use cert-manager to automatically issue and renew TLS certificates for your Kubernetes cluster. For more information, refer to the [MicroK8s documentation on cert-manager](https://microk8s.io/docs/addon-cert-manager).

Let's Encrypt certificates last 90 days, but cert-manager automatically renews them 30 days before expiry.

verify nginx ingress controller is installed:
kubectl get svc -n ingress-nginx

enable cert-manager:
microk8s enable cert-manager

apply cluster issuer:
kubectl apply -f letsencrypt-clusterissuer.yaml

verify cluster issuer by checking its status:
kubectl get clusterissuer letsencrypt-prod -o yaml

apply example ingress for dspaces:
kubectl apply -f example_dspaces_ingress.yaml


At this point, cert-manager will automatically request a certificate from Let's Encrypt and store it in a Kubernetes Secret named dspaces-tls.

verify certificate:
kubectl get certificate -n dspaces
kubectl get secret -n dspaces dspaces-tls





# Optional
Relavant code is inside /archive

If you have existing credentials: you can follow what's below:
To package the provided credentials (`fullchain.pem` and `privkey.pem`) into a Kubernetes Secret and reference them in the Ingress with the host field, follow these steps:

### Prerequisites

Ensure that your domain resolves to the external IP of your NGINX Ingress controller's load balancer service.

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
