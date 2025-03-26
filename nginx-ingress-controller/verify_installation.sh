# Verify that the ingress controller pods are running
kubectl get pods -n ingress-nginx

# Check the ingress controller service and get the external IP
kubectl get svc -n ingress-nginx
