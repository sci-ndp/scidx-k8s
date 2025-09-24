RELEASE_NAME ?= strimzi
NAMESPACE ?= kafka
CHART_VERSION ?= 0.45.0
CHART ?= strimzi/strimzi-kafka-operator
HELM_REPO_NAME ?= strimzi
HELM_REPO_URL ?= https://strimzi.io/charts

.PHONY: help repo repo-update namespace install uninstall search status

help:
	@printf "Targets:\n"
	@printf "  repo          Add the Strimzi Helm repo (idempotent).\n"
	@printf "  repo-update   Refresh Helm repo metadata.\n"
	@printf "  install       Install or upgrade the Strimzi operator.\n"
	@printf "  uninstall     Remove the Strimzi operator release.\n"
	@printf "  search        List available Strimzi Helm chart versions.\n"
	@printf "  status        Show release status in namespace $(NAMESPACE).\n"

repo:
	helm repo add $(HELM_REPO_NAME) $(HELM_REPO_URL) --force-update

repo-update: repo
	helm repo update

namespace:
	@kubectl get namespace $(NAMESPACE) >/dev/null 2>&1 || kubectl create namespace $(NAMESPACE)

install: repo-update namespace
	helm upgrade --cleanup-on-fail --install $(RELEASE_NAME) $(CHART) \
	  --version $(CHART_VERSION) \
	  --namespace $(NAMESPACE) \
	  --set watchNamespaces={$(NAMESPACE)}

uninstall:
	helm uninstall $(RELEASE_NAME) -n $(NAMESPACE)

search:
	helm search repo $(CHART) --versions

status:
	helm status $(RELEASE_NAME) -n $(NAMESPACE)
