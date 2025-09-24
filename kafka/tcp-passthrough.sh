#!/bin/bash
# Configure tcp passthrough for kafka brokers via nginx ingress controller in microk8s cluster
cat <<'EOF' | kubectl apply -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-ingress-tcp-microk8s-conf
  namespace: ingress
data:
  "31090": "kafka/scidx-kafka-kafka-0:9094"
  "31091": "kafka/scidx-kafka-kafka-1:9094"
  "31092": "kafka/scidx-kafka-kafka-2:9094"
  "31093": "kafka/scidx-kafka-kafka-3:9094"
EOF