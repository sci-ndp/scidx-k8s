#!/bin/bash

# Add the Strimzi Helm repository to your local Helm client
helm repo add strimzi https://strimzi.io/charts
# output example:
# '"strimzi" has been added to your repositories'

# Update your local Helm chart repository cache
helm repo update
