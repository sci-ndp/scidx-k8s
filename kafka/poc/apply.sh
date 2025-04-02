#!/bin/bash

# Apply namespace first
kubectl apply -f namespace.yaml

# Wait until the namespace exists before proceeding
echo "Waiting for namespace 'kafka' to be available..."
while ! kubectl get namespace kafka > /dev/null 2>&1; do
  sleep 1
done
echo "Namespace 'kafka' is ready"

# Apply all other resources
kubectl apply -f .
