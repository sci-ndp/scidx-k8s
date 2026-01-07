# Load overrides
CONFIG_FILE ?= config.mk
-include $(CONFIG_FILE)

# Kubernetes context
DEFAULT_KUBE_CONTEXT := $(shell kubectl config current-context 2>/dev/null)
ifeq ($(strip $(KUBE_CONTEXT)),)
KUBE_CONTEXT := $(if $(DEFAULT_KUBE_CONTEXT),$(DEFAULT_KUBE_CONTEXT),microk8s)
endif
KUBECTL := kubectl $(if $(KUBE_CONTEXT),--context $(KUBE_CONTEXT))
HELM ?= helm
HELM_CTX = $(if $(KUBE_CONTEXT),--kube-context $(KUBE_CONTEXT),)

# Strimzi operator settings
RELEASE_NAME ?= strimzi
NAMESPACE ?= kafka
CHART_VERSION ?= 0.45.0
CHART ?= strimzi/strimzi-kafka-operator
HELM_REPO_NAME ?= strimzi
HELM_REPO_URL ?= https://strimzi.io/charts

# Broker connection used for quick verification via kcat
BROKER_HOST ?= kafka-broker.example.com
BROKER_PORT ?= 31090
BROKER ?= $(BROKER_HOST):$(BROKER_PORT)

.PHONY: install verify uninstall tcp-passthrough-helm tcp-passthrough-microk8s namespace repo repo-update install-operator uninstall-operator search status-operator patch-advertised-host


# Cluster install/uninstall (assumes operator already running)
install: namespace patch-advertised-host
	$(KUBECTL) apply -f kafka-cluster-kraft.yaml -n $(NAMESPACE)

uninstall:
	$(KUBECTL) delete -f kafka-cluster-kraft.yaml -n $(NAMESPACE)


# Setup TCP passthrough for Kafka brokers via NGINX Ingress Controller
# for helm-based nginx ingress controller installation
tcp-passthrough-helm:
	$(HELM) $(HELM_CTX) upgrade --install ingress-nginx ingress-nginx/ingress-nginx \
		--namespace ingress-nginx --create-namespace \
		--set controller.service.type=LoadBalancer \
		--set tcp.31090="kafka/scidx-kafka-scidx-kafka-brokers-0:9094" \
		--set tcp.31091="kafka/scidx-kafka-scidx-kafka-brokers-1:9094" \
		--set tcp.31092="kafka/scidx-kafka-scidx-kafka-brokers-2:9094" \
		--set tcp.31093="kafka/scidx-kafka-scidx-kafka-brokers-3:9094"

tcp-passthrough-microk8s:
	printf '%s\n' \
	  "apiVersion: v1" \
	  "kind: ConfigMap" \
	  "metadata:" \
	  "  name: nginx-ingress-tcp-microk8s-conf" \
	  "  namespace: ingress" \
	  "data:" \
	  "  \"31090\": \"kafka/scidx-kafka-scidx-kafka-brokers-0:9094\"" \
	  "  \"31091\": \"kafka/scidx-kafka-scidx-kafka-brokers-1:9094\"" \
	  "  \"31092\": \"kafka/scidx-kafka-scidx-kafka-brokers-2:9094\"" \
	  "  \"31093\": \"kafka/scidx-kafka-scidx-kafka-brokers-3:9094\"" \
	| $(KUBECTL) apply -f -


# Strimzi Operator lifecycle
namespace:
	@$(KUBECTL) get namespace $(NAMESPACE) >/dev/null 2>&1 || $(KUBECTL) create namespace $(NAMESPACE)

repo:
	$(HELM) repo add $(HELM_REPO_NAME) $(HELM_REPO_URL) --force-update

repo-update: repo
	$(HELM) repo update

install-operator: repo-update namespace
	$(HELM) $(HELM_CTX) upgrade --install $(RELEASE_NAME) $(CHART) \
	  --version $(CHART_VERSION) \
	  --namespace $(NAMESPACE) \
	  --set watchAllNamespaces=true \
	  --wait

uninstall-operator:
	$(HELM) $(HELM_CTX) uninstall $(RELEASE_NAME) -n $(NAMESPACE)

search:
	$(HELM) search repo $(CHART) --versions

status-operator:
	$(HELM) $(HELM_CTX) status $(RELEASE_NAME) -n $(NAMESPACE)