kubectl patch deployment -n ingress-nginx nginx-ingress-ingress-nginx-controller --type='json' -p='[
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/args/-",
    "value": "--tcp-services-configmap=ingress-nginx/ingress-nginx-tcp"
  }
]'