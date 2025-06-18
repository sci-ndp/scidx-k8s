#!/bin/bash

# Apply namespace first
echo "Applying namespace from pop-namespace.yaml..."
kubectl apply -f pop-namespace.yaml

# Wait until the namespace exists before proceeding
echo "Waiting for namespace 'pop' to be available..."
while ! kubectl get namespace pop > /dev/null 2>&1; do
  sleep 1
done
echo "Namespace 'pop' is ready"

# Apply the pop-env-secret.yaml next
echo "Applying pop-env-secret.yaml..."
if [ -f "pop-env-secret.yaml" ]; then
  kubectl apply -f pop-env-secret.yaml
else
  echo "Error: pop-env-secret.yaml not found. Please create it using copy-secret.sh before proceeding."
  exit 1
fi

# Apply all other files in the current directory that start with 'pop'
# (e.g., pop-deployment.yaml, pop-service.yaml, pop-ingress.yaml)
# Exclude pop-namespace.yaml and pop-env-secret.yaml to avoid re-applying
echo "Applying remaining manifests (pop-deployment.yaml, pop-service.yaml, pop-ingress.yaml, etc.)..."
for file in pop*.yaml; do
  if [ "$file" != "pop-namespace.yaml" ] && [ "$file" != "pop-env-secret.yaml" ]; then
    if [ -f "$file" ]; then
      echo "Applying $file..."
      kubectl apply -f "$file"
    fi
  fi
done

echo "All manifests applied successfully."