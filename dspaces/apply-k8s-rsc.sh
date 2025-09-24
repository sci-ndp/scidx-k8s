#!/bin/bash

# Apply namespace first
kubectl apply -f dspaces-namespace.yaml

# Wait until the namespace exists before proceeding
echo "Waiting for namespace 'dspaces' to be available..."
while ! kubectl get namespace dspaces > /dev/null 2>&1; do
  sleep 1
done
echo "Namespace 'dspaces' is ready"

# Apply all other resources
kubectl apply -f .
