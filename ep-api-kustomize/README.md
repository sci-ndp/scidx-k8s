# NDP Endpoint – Kustomize

Lightweight Kustomize overlays for deploying the National Data Platform Endpoint (NDP-EP) API across `dev`, `test`, and `prod` environments.

## Prerequisites
- `kubectl` 1.21 or newer (includes `kubectl apply -k` support)
- Access to the target cluster/context with permission to create namespaces, secrets, and workloads

## Layout
- `kustomize/base`: shared manifests (deployment, service, ingress)
- `kustomize/overlays/<env>`: environment-specific namespace plus secret generator

## Configure Overlay (Ingress + Secrets)
1. Change into the overlay you plan to deploy:
   ```bash
   cd kustomize/overlays/prod   # or kustomize/overlays/(dev|test)
   ```

2. Update the ingress settings for your cluster in `ingress-patch.yaml`:
   ```bash
   vi ingress-patch.yaml
   ```
   See [Ingress Patch Details](#ingress-patch-details).

3. Copy the secret template to create your local secret file:
   ```bash
   cp ndp-ep-env-secret.env.template ndp-ep-env-secret.env
   ```

4. Then open `./ndp-ep-env-secret.env` and set values
   ```bash
   vi ndp-ep-env-secret.env
   ```
   Fill out the needed fields;<br>For details and examples, see [Secret Example](#secret-example).

## Dry Run (optional)
- Render manifests locally:
  ```bash
  kubectl kustomize kustomize/overlays/<env>
  ```
- Compare against the cluster without applying changes:
  ```bash
  kubectl apply --dry-run=server -k kustomize/overlays/<env>
  ```

## Deploy

> Note:<br>Namespaces are managed per overlay (`ndp-ep-dev`, `ndp-ep-test`, `ndp-ep`).<br><br>
What this does:<br>Kustomize creates the namespace (if needed), builds the secret from your `ndp-ep-env-secret.env`, and applies the shared resources.
```bash
kubectl apply -k .
```

## Cleanup
Remove everything defined in an overlay:

```bash
kubectl delete -k kustomize/overlays/<env>
```

## Next Steps
Go back to [**SciDx Kubernetes Document**](https://github.com/sci-ndp/scidx-k8s?tab=readme-ov-file#deploy-ndp-endpoint-api) for more details about the overall Kubernetes setup for SciDx service.

<br>

## Ingress Patch Details

`spec.ingressClassName`: set this to your cluster's ingress class (default: **public**).

`spec.rules[0].host`: set this to your public DNS name for the ingress controller.

> Note: <br>Default ingress path is `/api`, so your NDP endpoint API is served at `your-hostname/api`. To use a different root, edit `ROOT_PATH` in **overlays/(env)/kustomization.yaml (`configMapGenerator`)**. The replacement there updates the ingress path.

Example:
```yaml
- op: replace
  path: /spec/ingressClassName
  value: nginx # your ingress class name
- op: replace
  path: /spec/rules/0/host
  value: api.example.org # your public DNS name
```
[Back to `Configure Overlay (Ingress + Secrets)`](#configure-overlay-ingress--secrets)

<br>

## Secret Example

Prepare environment variables for NDP Endpoint API configuration:

> The file stays local (ignored by Git) and is converted into a Kubernetes secret at deploy time.

```bash
# API CONFIGURATION

# ==============================================
# ORGANIZATION SETTINGS
# ==============================================
# Your organization name for identification and metrics
ORGANIZATION="My organization"

# Endpoint name for identification in metrics and monitoring
EP_NAME="EP Name"

# ==============================================
# METRICS CONFIGURATION
# ==============================================
# Interval in seconds for sending metrics (default: 3300 seconds = 55 minutes)
METRICS_INTERVAL_SECONDS=3300

# ==============================================
# AUTHENTICATION CONFIGURATION
# ==============================================
# URL for the authentication API to retrieve user information
# This endpoint is used to validate tokens and fetch user details
AUTH_API_URL=https://idp.nationaldataplatform.org/temp/information

# ==============================================
# ACCESS CONTROL (Optional)
# ==============================================
# Enable organization-based access control (True/False)
# When enabled, only users belonging to the configured ORGANIZATION
# can perform POST, PUT, DELETE operations. Other authenticated users
# will receive 403 Forbidden on write operations.
# GET endpoints remain public regardless of this setting.
ENABLE_ORGANIZATION_BASED_ACCESS=False

# ==============================================
# LOCAL CATALOG CONFIGURATION
# ==============================================
# Choose your local catalog backend: "ckan" or "mongodb"
# Global and Pre-CKAN always use CKAN regardless of this setting
LOCAL_CATALOG_BACKEND=ckan

# ==============================================
# LOCAL CKAN CONFIGURATION (if LOCAL_CATALOG_BACKEND=ckan)
# ==============================================
# Enable or disable the local CKAN instance (True/False)
# Set to True if you have your own CKAN installation
CKAN_LOCAL_ENABLED=True

# Base URL of your local CKAN instance (Required if CKAN_LOCAL_ENABLED=True)
# Example: http://192.168.1.134:5000/ or https://your-ckan-domain.com/
CKAN_URL=http://XXX.XXX.XXX.XXX:XXXX/

# API Key for CKAN authentication (Required if CKAN_LOCAL_ENABLED=True)
# Get this from your CKAN user profile -> API Tokens
CKAN_API_KEY=

# ==============================================
# MONGODB CONFIGURATION (if LOCAL_CATALOG_BACKEND=mongodb)
# ==============================================
# MongoDB connection string
MONGODB_CONNECTION_STRING=mongodb://localhost:27017

# MongoDB database name for local catalog
MONGODB_DATABASE=ndp_local_catalog

# ==============================================
# PRE-CKAN CONFIGURATION
# ==============================================
# Enable or disable the Pre-CKAN instance (True/False)
# Set to True if you want to submit datasets to NDP Central Catalog
PRE_CKAN_ENABLED=False

# URL of the Pre-CKAN staging instance (Required if PRE_CKAN_ENABLED=True)
# This is typically provided by the NDP team
PRE_CKAN_URL=http://XX.XX.XX.XXX:5000/

# API key for Pre-CKAN authentication (Required if PRE_CKAN_ENABLED=True)
# Obtain this from the NDP team or your Pre-CKAN user profile
PRE_CKAN_API_KEY=

# ==============================================
# STREAMING CONFIGURATION
# ==============================================
# Enable or disable Kafka connectivity (True/False)
# Set to True if you want to ingest data from Kafka streams
KAFKA_CONNECTION=True

# Kafka broker hostname or IP address (Required if KAFKA_CONNECTION=True)
KAFKA_HOST=

# Kafka broker port number (Required if KAFKA_CONNECTION=True)
# Default Kafka port is 9092
KAFKA_PORT=9092

# ==============================================
# DEVELOPMENT & TESTING
# ==============================================
# Test token for development purposes (Optional)
# Leave blank in production environments for security
TEST_TOKEN=testing_token

# ==============================================
# EXTERNAL SERVICE INTEGRATIONS
# ==============================================
# Enable or disable JupyterLab integration (True/False)
# Set to True if you want to integrate with a JupyterLab instance
USE_JUPYTERLAB=False

# URL to your JupyterLab instance (Required if USE_JUPYTERLAB=True)
# Example: https://jupyter.your-domain.com or http://localhost:8888
JUPYTER_URL=

# ==============================================
# S3 STORAGE CONFIGURATION
# ==============================================
# Enable or disable S3 storage (True/False)
S3_ENABLED=True

# S3 endpoint (host:port) - use your S3-compatible service endpoint
S3_ENDPOINT=XXX.XXX.XXX.XXX:9000

# S3 access credentials
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin123

# Use secure connection (True for HTTPS, False for HTTP)
S3_SECURE=False

# Default region
S3_REGION=us-east-1
```

### Common Configuration Scenarios

#### Scenario 1: NDP Central Catalog Only (Read-Only)
```bash
# Minimal configuration for read-only access to NDP Central Catalog
ORGANIZATION="Your Organization"
CKAN_LOCAL_ENABLED=False
PRE_CKAN_ENABLED=False
KAFKA_CONNECTION=False
USE_JUPYTERLAB=False
```

#### Scenario 2: Local CKAN Development
```bash
# Configuration for local CKAN development
ORGANIZATION="Your Organization"
LOCAL_CATALOG_BACKEND=ckan
CKAN_LOCAL_ENABLED=True
CKAN_URL=http://localhost:5000/
CKAN_API_KEY=your-local-ckan-api-key
PRE_CKAN_ENABLED=False
TEST_TOKEN=dev_token
```

#### Scenario 3: MongoDB Local Catalog (No CKAN Required)
```bash
# Lightweight setup with MongoDB backend
ORGANIZATION="Your Organization"
LOCAL_CATALOG_BACKEND=mongodb
MONGODB_CONNECTION_STRING=mongodb://localhost:27017
MONGODB_DATABASE=ndp_local_catalog
PRE_CKAN_ENABLED=False
TEST_TOKEN=dev_token
```

#### Scenario 4: Full NDP Integration with CKAN
```bash
# Complete setup with local CKAN and NDP submission capability
ORGANIZATION="Your Organization"
CKAN_LOCAL_ENABLED=True
CKAN_URL=http://your-ckan-instance:5000/
CKAN_API_KEY=your-local-ckan-api-key
PRE_CKAN_ENABLED=True
PRE_CKAN_URL=https://preckan.nationaldataplatform.org
PRE_CKAN_API_KEY=your-ndp-preckan-api-key
```

[Back to `Configure Overlay (Ingress + Secrets)`](#configure-overlay-ingress--secrets)
