# COMPOSE_FILE=docker-compose.dev.yaml

default: deploy-test

deploy-test:
	 cd ndp-hub && python generate_values.py --env test
	 helm upgrade --cleanup-on-fail --install ndp-hub ndp-hub --kube-context nautilus --namespace ndp-test --values ndp-hub/_values_test.yaml
deploy-staging:
	 cd ndp-hub && python generate_values.py --env staging
	 helm upgrade --cleanup-on-fail --install ndp-hub ndp-hub --kube-context nautilus --namespace ndp-staging --values ndp-hub/_values_staging.yaml
deploy-prod:
	 cd ndp-hub && python generate_values.py --env prod
	 helm upgrade --cleanup-on-fail --install ndp-hub ndp-hub --kube-context arn:aws:eks:us-west-2:515966508187:cluster/sci --namespace jupyterhub --values ndp-hub/_values_prod.yaml
