helm install kafka bitnami/kafka \
  --namespace default \
  -f kafka-values.yaml

# Check if the Kafka pods are running
# Expect 3 Kafka brokers (kafka-0, kafka-1, kafka-2) and three ZooKeeper pods
# kubectl get pods -n default -l app.kubernetes.io/name=kafka