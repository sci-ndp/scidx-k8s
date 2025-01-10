# This script generates a k8s Secret manifest file named pop-env-secret.yaml.
# The secret is created from environment variables stored in the 'env_variables' directory, 
# located within the 'pop' project. 
# Note: This command performs a dry run and does not apply the secret directly to the cluster. 
# The generated YAML file is intended for review or manual deployment to a k8s cluster.
kubectl create secret generic pop-env-secret --from-file=env_variables -o yaml --dry-run=client > pop-env-secret.yaml
