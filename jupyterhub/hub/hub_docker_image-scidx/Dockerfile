# hub.image -> runs the JupyterHub service (auth, spawner, proxy)

# Base image source: https://hub.docker.com/r/jupyterhub/k8s-hub
FROM jupyterhub/k8s-hub:4.2.0

COPY templates/403.html /etc/jupyterhub/custom/403.html
COPY templates/page.html /etc/jupyterhub/custom/page.html

COPY pics/scidx_logo.png /usr/local/share/jupyterhub/static/images/scidx_logo.png


RUN pip install kubernetes

# In jupyterhub/helm/config.yaml:
# jupyterhub:
#  hub:
#    image:
#      name: yutianqin/scidx-k8s-hub
#      tag: "<version>"