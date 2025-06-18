#!/bin/bash

# Define the namespace
NAMESPACE="kafka"

# Check if the namespace exists
if ! kubectl get namespace "$NAMESPACE" >/dev/null 2>&1; then
  echo "Namespace $NAMESPACE not found. Creating..."
  kubectl create namespace "$NAMESPACE"
else
  echo "Namespace $NAMESPACE already exists."
fi

helm install strimzi strimzi/strimzi-kafka-operator \
  --namespace "$NAMESPACE" \
  --set watchNamespaces={$NAMESPACE} # Configure the operator to only manage resources in the kafka namespace
