# This script creates a k8s TLS secret named 'dspaces-tls-secret' in the 'dspaces' namespace.
# The secret is created using the private key file 'privkey.pem' and the certificate file 'fullchain.pem'.
# Usage:
#   Ensure that 'privkey.pem' and 'fullchain.pem' are present in the current directory.
#   Run this script to create the TLS secret in the specified namespace.
kubectl create secret tls dspaces-tls-secret \
  --key privkey.pem \
  --cert fullchain.pem \
  -n dspaces
  