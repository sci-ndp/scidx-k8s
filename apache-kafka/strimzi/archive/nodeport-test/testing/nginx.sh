#!/bin/bash

# Define the namespace
NAMESPACE="ingress-nginx"

# Check if the namespace exists
if ! kubectl get namespace "$NAMESPACE" >/dev/null 2>&1; then
  echo "Namespace $NAMESPACE not found. Creating..."
  kubectl create namespace "$NAMESPACE"
else
  echo "Namespace $NAMESPACE already exists."
fi

# Install the NGINX ingress controller with a LoadBalancer service type
# helm install nginx-ingress ingress-nginx/ingress-nginx \
#   --namespace "$NAMESPACE" \
#   --set controller.service.type=LoadBalancer
  
helm install nginx-ingress ingress-nginx/ingress-nginx \
    --namespace $NAMESPACE \
    --set controller.service.type=NodePort \
    --set controller.service.nodePorts.http=32080 \
    --set controller.service.nodePorts.https=32443 \
    --set controller.extraArgs.enable-ssl-passthrough=true
