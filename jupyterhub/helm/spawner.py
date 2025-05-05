from oauthenticator.generic import GenericOAuthenticator
from kubespawner import KubeSpawner
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException
from tornado.web import HTTPError
import requests
import logging
import http.client
import base64
import socket
import json
import os


# Configure a logger for debugging
log = logging.getLogger("jupyterhub.auth")
log.setLevel(logging.DEBUG)

# Function to retrieve Keycloak client credentials from Kubernetes secret
def use_k8s_secret(namespace, secret_name):
    config.load_incluster_config()
    v1 = client.CoreV1Api()

    # Get the secret values
    secret = v1.read_namespaced_secret(name=secret_name, namespace=namespace)
    secret_data = secret.data
    value = base64.b64decode(secret_data['values.yaml']).decode('utf-8')

    client_id_splitted = value.split('client_secret: ')[0].split('client_id: ')[1]  # isolate cliect_secret_value
    client_id_splitted = client_id_splitted.split('\n')[0]  # cut \n

    client_secret_splitted = value.split('client_secret: ')[1]  # isolate cliect_secret_value
    client_secret_splitted = client_secret_splitted[:-1]  # cut \n

    return client_id_splitted, client_secret_splitted

NAMESPACE = 'jupyterhub'
CLIENT_ID, CLIENT_SECRET = use_k8s_secret(namespace=NAMESPACE, secret_name='jupyterhub-secret')
KEYCLOAK_URL = "https://idp-test.nationaldataplatform.org"
NDP_EXT_VERSION = '0.0.12'
CKAN_API_URL = "https://nationaldataplatform.org/catalog/api/3/action/"
WORKSPACE_API_URL = "https://nationaldataplatform.org/workspaces-api"
REFRESH_EVERY_SECONDS = 1200

# Custom Authenticator for Keycloak token refresh
class MyAuthenticator(GenericOAuthenticator):
    async def refresh_user(self, user, handler):
        print(f"Refreshing Authenticator refresh_user for {user.name}")
        log.debug(f"[refresh_user] start for {user.name}")
        auth_state = await user.get_auth_state()
        log.debug(f"[refresh_user] auth_state keys: {list((auth_state or {}).keys())}")
        if auth_state:
            if not await self.check_and_refresh_tokens(user, auth_state):
                log.warning(f"[refresh_user] token refresh failed for {user.name}")
                if handler:
                    # print(f'Redirecting to logout')
                    print ("Cleaning up cookies")
                    handler.clear_cookie("jupyterhub-hub-login")
                    handler.clear_cookie("jupyterhub-session-id")
                    # handler.redirect('/hub/logout')
                    # print(f'Redirected to logout')
                    raise HTTPError(401, "Your session has expired. Please log out and log in again.")
                    # Optionally, you can stop further processing
                    # handler.finish()
                    # return False
            else:
                log.debug(f"[refresh_user] token refreshed for {user.name}")
        return True

    async def check_and_refresh_tokens(self, user, auth_state):
        refresh_token_valid = self.check_refresh_token_keycloak(auth_state)
        # print(f'refresh_token_valid: {refresh_token_valid}')
        log.debug(f"[check_and_refresh_tokens] refresh_token_valid = {bool(refresh_token_valid)}")
        if refresh_token_valid:
            # here we need to refresh access_token
            print('Trying to refresh access_token')
            log.debug("[check_and_refresh_tokens] trying to refresh access_token")
            auth_state['access_token'], auth_state['refresh_token'] = refresh_token_valid
            await user.save_auth_state(auth_state)
            print(f"Updated auth_state saved for {user.name}")
            log.debug(f"[check_and_refresh_tokens] updated auth_state saved for {user.name}")
            return True
        else:
            log.debug(f"[check_and_refresh_tokens] no valid refresh token")
            return False

    def check_refresh_token_keycloak(self, auth_state):
        """
        Will return tuple of access_token and refresh_token if refresh is possible, or False otherwise
        :param auth_state:
        :return:
        """
        _access_token = auth_state.get('access_token')
        _refresh_token = auth_state.get('refresh_token')
        print(f"Checking refresh_token")
        log.debug("[check_refresh_token_keycloak] checking refresh_token …")
        response = requests.post(f"{KEYCLOAK_URL}/realms/NDP/protocol/openid-connect/token",
                                 data={
                                     'grant_type': 'refresh_token',
                                     'refresh_token': _refresh_token,
                                     'client_id': CLIENT_ID,
                                     'client_secret': CLIENT_SECRET
                                 })
        log.debug(f"[check_refresh_token_keycloak] response.status_code = {response.status_code}")
        if response.status_code == 200:
            print(f"Refresh token is still good!")
            log.debug("[check_refresh_token_keycloak] refresh token good")
            new_access_token = response.json().get('access_token')
            new_refresh_token = response.json().get('refresh_token')
            return new_access_token, new_refresh_token
        else:
            log.warning("[check_refresh_token_keycloak] refresh token invalid or expired")
            return False

# pass access_token and refresh_token for communicating with NDP APIs
def auth_state_hook(spawner, auth_state):
    spawner.access_token = auth_state['access_token']
    spawner.refresh_token = auth_state['refresh_token']
    spawner.environment.update({'ACCESS_TOKEN': spawner.access_token})
    spawner.environment.update({'REFRESH_TOKEN': spawner.refresh_token})

## Functions to retrieve user groups
async def get_user_groups(token):
    try:
        conn = http.client.HTTPSConnection("nationaldataplatform.org")
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'}
        conn.request("GET", "/workspaces-api/group", headers=headers)
        response = conn.getresponse()
        if response.status != 200:
            return []
        data = json.loads(response.read().decode("utf-8"))
        return data
    except (http.client.HTTPException, TimeoutError, json.JSONDecodeError, socket.timeout):
        return []

async def pre_spawn_hook(spawner):
    config.load_incluster_config()
    api = client.CoreV1Api()
    # Reset the profile list to ensure custom image is not retained

    # pip install jupyterlab-launchpad
    pip_install_command0 = ("pip uninstall jupyterlab-git -y")
    pip_install_command1 = ("pip install --upgrade jupyterlab==4.2.4 jupyter-archive==3.4.0 jupyterlab-launchpad==1.0.1")
    pip_install_command2 = ("pip install jupyterlab-git==0.50.1 --index-url https://gitlab.nrp-nautilus.io/api/v4/projects/3930/packages/pypi/simple --user")
    pip_install_command3 = (f"pip install ndp-jupyterlab-extension=={NDP_EXT_VERSION} --index-url https://gitlab.nrp-nautilus.io/api/v4/projects/3930/packages/pypi/simple --user")

    # Modify the spawner's start command to include the pip install
    original_cmd = spawner.cmd or ["jupyterhub-singleuser"]
    spawner.cmd = [
        "bash",
        "-c",
        f"{pip_install_command0} || true "
        f"&& {pip_install_command1} || true "
        f"&& {pip_install_command2} || true "
        f"&& {pip_install_command3} || true "
        f"&& cd /home/jovyan/work || true "
        f"&& exec {' '.join(original_cmd)}"
    ]

    # make username available for MLflow library
    username = spawner.user.name
    spawner.environment.update({'MLFLOW_TRACKING_USERNAME': username})
    spawner.environment.update({"CKAN_API_URL": CKAN_API_URL})
    spawner.environment.update({"WORKSPACE_API_URL": WORKSPACE_API_URL})
    spawner.environment.update({"REFRESH_EVERY_SECONDS": str(REFRESH_EVERY_SECONDS)})

    try:
        groups = await get_user_groups(spawner.access_token)
        if groups:
            id_lst = []
            init_containers = []
            for group in groups:
                group_id = group['subgroup_id']
                group_type = group['type_of_entity']

                if group_id not in id_lst and group_type == 'data_challenge':
                    id_lst.append(group_id)
                    id_short = group_id[0:13]
                    group_name = group['group_name'].replace(" ", "-")
                    pvc_name = f'claim-ndpgroups-{id_short}'
                    volume_name = f'volume-ndpgroups-{id_short}'
                    try:
                        api.read_namespaced_persistent_volume_claim(name=pvc_name, namespace=NAMESPACE)
                    except ApiException as e:
                        print(e)
                        if e.status == 404:
                            print(f"Creating PVC {pvc_name}")
                            pvc_manifest = {
                                'apiVersion': 'v1',
                                'kind': 'PersistentVolumeClaim',
                                'metadata': {'name': pvc_name, 'namespace': NAMESPACE},
                                'spec': {
                                    'accessModes': ['ReadWriteMany'],
                                    'resources': {'requests': {'storage': '5Gi'}},
                                    'storageClassName': 'gp2'
                                }
                            }
                            api.create_namespaced_persistent_volume_claim(namespace=NAMESPACE, body=pvc_manifest)
                            print(f"PVC {pvc_name} created successfully.")
                        else:
                            print(f"Error creating PVC {pvc_name}: {e}!!!!!!")
                            raise
                    logging.info(f"Adding volume and mount for group {group_name}")
                    init_containers.append({
                        'name': f'set-permissions-{id_short}',
                        'image': 'alpine',
                        'command': ['sh', '-c', f'chmod -R 0777 /shared-storage/{group_name}-{id_short[0:5]}'],
                        'volumeMounts': [{
                            'name': volume_name,
                            'mountPath': f'/shared-storage/{group_name}-{id_short[0:5]}'
                        }]
                    })
                    spawner.volume_mounts.append({
                        'name': volume_name,
                        'mountPath': f'/home/jovyan/work/{group_name}-Shared-Storage-{id_short[0:5]}/'
                    })
                    spawner.volumes.append({
                        'name': volume_name,
                        'persistentVolumeClaim': {'claimName': pvc_name}
                    })
            spawner.extra_volumes = spawner.volumes
            spawner.extra_volume_mounts = spawner.volume_mounts
            spawner.extra_pod_config = spawner.extra_pod_config or {}
            spawner.extra_pod_config.setdefault('initContainers', []).extend(init_containers)
            spawner.environment.update({'USER_GROUPS': ','.join(groups)})
    except:
        pass

# Basic Spawner configuration
class MySpawner(KubeSpawner):
    notebook_dir = '/home/jovyan/work'

# JupyterHub configuration
c.JupyterHub.spawner_class = MySpawner
c.MySpawner.auth_state_hook = auth_state_hook
c.MySpawner.pre_spawn_hook = pre_spawn_hook
c.JupyterHub.authenticator_class = MyAuthenticator
c.MyAuthenticator.auth_refresh_age = 86300  # Refresh once per day
# c.MyAuthenticator.refresh_pre_spawn = True