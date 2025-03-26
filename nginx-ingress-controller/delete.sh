# Uninstall the nginx-ingress release in the ingress-nginx namespace
helm uninstall nginx-ingress -n ingress-nginx

# Delete the ingress-nginx namespace
kubectl delete namespace ingress-nginx

# Remove the ingress-nginx Helm repo (optional)
# helm repo remove ingress-nginx
