# Default target
.PHONY: default
default: deploy

# Variables
HELM_RELEASE := scidx-jhub # Name of the Helm release
HELM_CHART := . # Path to the Helm chart(./charts)
KUBE_CONTEXT := arn:aws:eks:us-west-2:515966508187:cluster/scidx # Kubernetes cluster context
NAMESPACE := jupyterhub
VALUES_FILE := config.yaml
# VALUES_FILE := config_diy.yaml

# Updates Helm chart dependencies by downloading them into the charts/ directory
.PHONY: update-dependency
update-dependency:
	helm dependency update

# Create a kubernetes secret for keycloak client_id and client_secret
.PHONY: create-jupyterhub-secret
create-jupyterhub-secret:
	@echo "Creating JupyterHub secret in namespace $(NAMESPACE)..."
	kubectl create secret generic jupyterhub-secret \
		--from-file=values.yaml=jupyterhub_secret.yaml \
		--namespace $(NAMESPACE)

# Delete the kubernetes secret for keycloak client_id and client_secret
.PHONY: delete-jupyterhub-secret
delete-jupyterhub-secret:
	@echo "Deleting JupyterHub secret in namespace $(NAMESPACE)..."
	kubectl delete secret jupyterhub-secret --namespace $(NAMESPACE) || true

# Generate the config.yaml file by embedding spawner.py into values.yaml
.PHONY: generate
generate:
	@echo "Generating $(VALUES_FILE)..."
	python generate_config.py

# Clean up generated config.yaml files
.PHONY: clean
clean:
	@echo "Cleaning up generated files..."
	rm -f $(VALUES_FILE)

# Deploy the Helm chart
.PHONY: deploy
deploy:
	@echo "Deploying $(HELM_RELEASE) to $(NAMESPACE)..."
	helm upgrade --cleanup-on-fail \
		--install $(HELM_RELEASE) $(HELM_CHART) \
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
	@echo "Fetching Ingress details for $(HELM_RELEASE) ..."
	@kubectl get ingress -n $(NAMESPACE) -o wide
