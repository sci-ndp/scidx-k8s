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

# Install the Strimzi Kafka Operator using the provided URL
kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' --namespace $NAMESPACE

# Check if the installation was successful
if [ $? -eq 0 ]; then
  echo "Strimzi Kafka Operator installed successfully."
else
  echo "Failed to install Strimzi Kafka Operator."
  exit 1
fi