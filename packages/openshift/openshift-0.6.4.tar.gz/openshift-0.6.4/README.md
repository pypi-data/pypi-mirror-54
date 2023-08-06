# OpenShift python client

[![Build Status](https://travis-ci.org/openshift/openshift-restclient-python.svg?branch=master)](https://travis-ci.org/openshift/openshift-restclient-python)
[![Coverage Status](https://coveralls.io/repos/github/openshift/openshift-restclient-python/badge.svg?branch=master)](https://coveralls.io/github/openshift/openshift-restclient-python?branch=master)

Python client for the [OpenShift](http://openshift.redhat.com/) API.

## Installation

From source:

```
git clone https://github.com/openshift/openshift-restclient-python.git
cd openshift-restclient-python
python setup.py install
```

From [PyPi](https://pypi.python.org/pypi/openshift/) directly:

```
pip install openshift
```

Using [Dockerfile](Dockerfile):

```
docker build -t openshift-restclient-python -f Dockerfile .
```

## Usage and examples

The OpenShift client depends on the [Kubernetes Python client](https://github.com/kubernetes-incubator/client-python.git), and as part of the installation process, the Kubernetes (K8s) client is automatically installed.

In the case you are using Docker, you will likely need to share your `.kube/config` with the `openshift-restclient-python` container:

```
docker run -it -v $HOME/.kube/config:/root/.kube/config:z openshift-restclient-python python
```

There are two ways this project interacts with the OpenShift API. The first, now deprecated, is to use models and functions generated with swagger from the API spec. The second, new approach, is
to use a single model and client to generically interact with all resources on the server. The dynamic client also works with
resources that are defined by aggregated API servers or Custom Resource Definitions.

### Dynamic client usage

To work with the dynamic client, you will need an instantiated kubernetes client object. For example, the following uses the dynamic client to create a new Service object:

```python
import yaml
from kubernetes import client, config
from openshift.dynamic import DynamicClient

k8s_client = config.new_client_from_config()
dyn_client = DynamicClient(k8s_client)

v1_services = dyn_client.resources.get(api_version='v1', kind='Service')

service = """
kind: Service
apiVersion: v1
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
ports:
  - protocol: TCP
    port: 8080
    targetPort: 9376
"""

service_data = yaml.load(service)
resp = v1_services.create(body=service_data, namespace='default')

# resp is a ResourceInstance object
print(resp.metadata)
```

Now in the following example, we use the dynamic client to create a Route object, and associate it with the new Service:

```python
import yaml
from kubernetes import client, config
from openshift.dynamic import DynamicClient

k8s_client = config.new_client_from_config()
dyn_client = DynamicClient(k8s_client)

v1_routes = dyn_client.resources.get(api_version='route.openshift.io/v1', kind='Route')

route = """
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: frontend
spec:
  host: www.example.com
  to:
    kind: Service
    name: my-service
"""

route_data = yaml.load(route)
resp = v1_routes.create(body=route_data, namespace='default')

# resp is a ResourceInstance object
print(resp.metadata)
```

And finally, the following uses the dynamic client to list Projects the user can access:

```python
from kubernetes import client, config
from openshift.dynamic import DynamicClient

k8s_client = config.new_client_from_config()
dyn_client = DynamicClient(k8s_client)

v1_projects = dyn_client.resources.get(api_version='project.openshift.io/v1', kind='Project')

project_list = v1_projects.get()

for project in project_list.items:
    print(project.metadata.name)
```

### DEPRECATED Generated client usage

To work with a K8s object, use the K8s client, and to work with an OpenShift specific object, use the OpenShift client. For example, the following uses the K8s client to create a new Service object:

```python
import yaml
from kubernetes import client, config

config.load_kube_config()
api = client.CoreV1Api()

service = """
kind: Service
apiVersion: v1
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
ports:
  - protocol: TCP
    port: 8080
    targetPort: 9376
"""

service_data = yaml.load(service)
resp = api.create_namespaced_service(body=service_data, namespace='default')

# resp is a V1Service object
print resp.metadata.self_link
```

Now in the following example, we use the OpenShift client to create a Route object, and associate it with the new Service:

```python
import yaml
from openshift import client, config

config.load_kube_config()
api = client.OapiApi()

route = """
apiVersion: v1
kind: Route
metadata:
  name: frontend
spec:
  host: www.example.com
  to:
    kind: Service
    name: my-service
"""

route_data = yaml.load(route)
resp = api.create_namespaced_route(body=route_data, namespace='default')

# resp is a V1Route object
print resp.metadata.self_link
```

And finally, the following uses the OpenShift client to list Projects the user can access:

```python
from openshift import client, config

config.load_kube_config()
oapi = client.OapiApi()

project_list = oapi.list_project()
for project in project_list.items:
    print project.metadata.name
```

#### DEPRECATED Documentation

All OpenShift API and Model documentation can be found in the [Generated client's README file](openshift/README.md)

#### DEPRECATED  Update generated client

Updating the generated client requires the following tools:

- tox
- docker

To apply the updates:

1) Incorporate new changes to update scripts 
    - [scripts/constants.py](./scripts/constants.py), [scripts/pom.xml](./scripts/pom.xml), [scripts/preprocess_spec.py](./scripts/preprocess_spec.py), and [update-client.sh](./update-client.sh) are the most important
2) Run tox -e update_client

## Compatibility

We are downstream of the [kubernetes python client](github.com/kubernetes-client/python). We maintain compatibility for API version `n-2` - so if you are connecting to a version 3.6 OpenShift cluster, the list of supported python client versions would be `[0.3.x, 0.4.x, 0.5.x]`.

#### Compatibility matrix

| openshift python | kubernetes python | Kubernetes 1.5 | Kubernetes 1.6 | Kubernetes 1.7 | Kubernetes 1.8 | Kubernetes 1.9 |
|------------------|-------------------|----------------|----------------|----------------|----------------|----------------|
|  openshift 0.3   |  kubernetes 3.0   | +              | +              | ✓              | -              | -              |
|  openshift 0.4   |  kubernetes 4.0   | +*             | +              | +              | ✓              | -              |
|  openshift 0.5   |  kubernetes 5.0   | +*             | +*             | +              | +              | ✓              |
|  openshift HEAD  |  kubernetes HEAD  | +*             | +*             | +              | +              | ✓              |

Key:

* `✓` Exactly the same features / API objects in both openshift-restclient-python and the OpenShift
  version.
* `+` openshift-restclient-python has features or api objects that may not be present in the
  OpenShift cluster, but everything they have in common will work.
* `-` The OpenShift cluster has features the openshift-restclient-python library can't use
  (additional API objects, etc).
* `*` This client/server combination may work, but is not officially supported. 

## Community, Support, Discussion

If you have any problem with the package or any suggestions, please file an [issue](https://github.com/openshift/openshift-restclient-python/issues).

### Code of Conduct

Participation in the Kubernetes community is governed by the [CNCF Code of Conduct](https://github.com/cncf/foundation/blob/master/code-of-conduct.md).


