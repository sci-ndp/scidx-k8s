# python generate_values.py
# helm upgrade --cleanup-on-fail --install scidx-jhub scidx-jhub --kube-context arn:aws:eks:us-west-2:515966508187:cluster/sci --create-namespace jupyterhub --values _values.yaml


# Default target
.PHONY: default
default: deploy

# Variables
HELM_RELEASE := scidx-jhub
HELM_CHART := .
KUBE_CONTEXT := arn:aws:eks:us-west-2:515966508187:cluster/sci
NAMESPACE := jupyterhub
VALUES_FILE := _values.yaml

# Generate the values file by embedding spawner.py into values.yaml
.PHONY: generate
generate:
	@echo "Generating $(VALUES_FILE)..."
	python generate_values.py

# Deploy the Helm chart
.PHONY: deploy
deploy: generate
	@echo "Deploying $(HELM_RELEASE) to $(NAMESPACE)..."
	helm upgrade --cleanup-on-fail --install $(HELM_RELEASE) $(HELM_CHART) \
		--kube-context $(KUBE_CONTEXT) \
		--namespace $(NAMESPACE) \
		--create-namespace \
		--values $(VALUES_FILE)

# Uninstall the Helm chart
.PHONY: uninstall
uninstall:
	@echo "Uninstalling $(HELM_RELEASE) from $(NAMESPACE)..."
	helm uninstall $(HELM_RELEASE) \
		--kube-context $(KUBE_CONTEXT) \
		--namespace $(NAMESPACE)

# Check the status of the Helm release
.PHONY: status
status:
	@echo "Checking status of $(HELM_RELEASE) in $(NAMESPACE)..."
	helm status $(HELM_RELEASE) \
		--kube-context $(KUBE_CONTEXT) \
		--namespace $(NAMESPACE)

# Get the Ingress IP for accessing JupyterHub
.PHONY: get-ingress
get-ingress:
	@echo "Fetching Ingress details for $(HELM_RELEASE) in $(NAMESPACE)..."
	@kubectl get ingress -n $(NAMESPACE) -o wide

# Clean up generated files
.PHONY: clean
clean:
	@echo "Cleaning up generated files..."
	rm -f $(VALUES_FILE)