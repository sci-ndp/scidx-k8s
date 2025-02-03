#!/bin/bash

# Apply namespace first
kubectl apply -f pop-namespace.yaml

# Wait until the namespace exists before proceeding
echo "Waiting for namespace 'pop' to be available..."
while ! kubectl get namespace pop > /dev/null 2>&1; do
  sleep 1
done
echo "Namespace 'pop' is ready"

# Apply all other resources
kubectl apply -f .
