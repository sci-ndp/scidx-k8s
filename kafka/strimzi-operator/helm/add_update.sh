#!/bin/bash

# Add the Strimzi Helm repository to your local Helm client
helm repo add strimzi https://strimzi.io/charts

# Update your local Helm chart repository cache
helm repo update
