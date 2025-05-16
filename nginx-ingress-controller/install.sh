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
helm upgrade --install nginx-ingress ingress-nginx/ingress-nginx \
  --namespace "$NAMESPACE" \
  --set controller.service.type=LoadBalancer
