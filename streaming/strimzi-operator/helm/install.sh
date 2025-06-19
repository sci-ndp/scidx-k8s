#!/bin/bash

# Define the namespace
NAMESPACE="kafka"
CHART_VERSION="0.45.0" # strimzi kafka operator 0.46.0 stop support for ZooKeeper-based Apache Kafka clusters and for KRaft migration

# Check if the namespace exists
if ! kubectl get namespace "$NAMESPACE" >/dev/null 2>&1; then
  echo "Namespace $NAMESPACE not found. Creating..."
  kubectl create namespace "$NAMESPACE"
else
  echo "Namespace $NAMESPACE already exists."
fi

# Install/upgrade the Strimzi Kafka Operator helm chart
helm upgrade --cleanup-on-fail \
  --install strimzi strimzi/strimzi-kafka-operator \
  --version "$CHART_VERSION" \
  --namespace "$NAMESPACE" \
  --set watchNamespaces={$NAMESPACE} # make strimzi operator only watch Kafka resource deployed in the $NAMESPACE namespace