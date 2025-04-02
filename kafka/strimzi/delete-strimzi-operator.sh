#!/bin/bash

# Define the namespace
NAMESPACE="kafka"

# Delete the Strimzi Kafka Operator resources
echo "Deleting Strimzi Kafka Operator resources from namespace $NAMESPACE..."
kubectl delete -f 'https://strimzi.io/install/latest?namespace=kafka' --namespace "$NAMESPACE" --ignore-not-found=true

# Check if the deletion was successful
if [ $? -eq 0 ]; then
  echo "Strimzi Kafka Operator resources deleted successfully."
else
  echo "Failed to delete Strimzi Kafka Operator resources."
  exit 1
fi

# Delete the namespace
echo "Deleting namespace $NAMESPACE..."
kubectl delete namespace "$NAMESPACE" --ignore-not-found=true

# Check if the namespace deletion was successful
if [ $? -eq 0 ]; then
  echo "Namespace $NAMESPACE deleted successfully."
else
  echo "Failed to delete namespace $NAMESPACE."
  exit 1
fi

echo "Cleanup completed."