Set up
1. use pop/generate-k8s-secret.sh to package the env var into a k8s secret resource
2. `sh apply-k8s-rsc.sh` to apply all .yaml manifests to the cluster(based on your current context)

Test
1. `kubectl get svc -n ingress-nginx` check external ip of ingress controller
2. open broswer then hit 'external-ip/pop' (e.g. ae51228b10e77418e9ea6a0b55954cc6-412054749.us-west-2.elb.amazonaws.com/pop)
   