---
title: kubernetes >  retrieve container image inventory
categories: kubernetes
---
We would be using kubectl and then write some Python code to retrieve the list of images of containers 
running in a GKE Kubernetes cluster. Some familiarity with YAML, Python, Kubectl and fundamentals of 
Kubernetes would be essential to understand the post better.

# Details of Pods
Lets view the list pods in all namespaces.
```
$ kubectl get po -A
NAMESPACE     NAME                                                        READY   STATUS    RESTARTS   AGE
kube-system   event-exporter-gke-564fb97f9-6bt5p                          2/2     Running   1          13m
kube-system   fluentbit-gke-2mfvq                                         2/2     Running   0          13m
kube-system   fluentbit-gke-s5cjj                                         2/2     Running   0          13m
---TRUNCATED--
```

We can get more information about the pods by viewing their details in yaml format.
```
$ kubectl get po -A -o yaml
apiVersion: v1
items:
- apiVersion: v1
  kind: Pod
  metadata:
    annotations:
      components.gke.io/component-name: event-exporter
      components.gke.io/component-version: 1.0.9
    creationTimestamp: "2021-03-18T11:33:52Z"
    generateName: event-exporter-gke-564fb97f9-
---TRUNCATED---
```

Let's save this info in a file.
```
$ kubectl get po -A -o yaml > /tmp/details-of-pods.yaml

$ cat /tmp/details-of-pods.yaml 
apiVersion: v1
items:
- apiVersion: v1
  kind: Pod
  metadata:
    annotations:
      components.gke.io/component-name: event-exporter
      components.gke.io/component-version: 1.0.9
    creationTimestamp: "2021-03-18T11:33:52Z"
    generateName: event-exporter-gke-564fb97f9-
---TRUNCATED---
```

# Retrive the images
Since we have the required data in a file, we can parse it to retrieve the info we need, in this case 
the image of containers.

Let's get into Python shell, and import the yaml package, that helps us parsing YAML content.
```
$ python3
Python 3.8.5 (default, Jan 27 2021, 15:41:15) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import yaml
```

We are now to going to read the file and create a new object that stores the YAML content as a 
dictionary object.
```
with open('/tmp/details-of-pods.yaml') as f:
    pod_list = yaml.load(f, Loader=yaml.FullLoader)
    print(type(pod_list))  
    # should print <class 'dict'>
```

What we now have is a dictionary object and we should be able to parse it using standard dictionary 
methods available in Python.
```
for key in pod_list:
    print(key)
    # should print
    ```
    apiVersion
    items
    kind
    metadata
    ```
```

There are 4 main keys in the dictionary, and we are interested in items, as that refers to the list of 
Pods. We can iterate over the items list, and each item would be a dictionary again as that refers to 
one complete Pod manifest.

Let's create a file, where we can store the results, we are retreiving.
```
file = open('/tmp/container-img-inventory.csv', 'w')
file.write('Pod Name\tPod Namespace\tContainer Name\tContainer Image\n')
```
Note that \t referes to tab \n refers to newline character.

```
for item in pod_list['items']:
    print(item.keys())
    # should print
    ```
    dict_keys(['apiVersion', 'kind', 'metadata', 'spec', 'status'])
    dict_keys(['apiVersion', 'kind', 'metadata', 'spec', 'status'])
    --TRUNCATED
    ```
```

In a Pod manifest, its name would be present in metadata.name, its namespace would be present in 
metadata.namespace, the spec of its containers would be present in spec.containers. Let's check a 
sample Pod manifest for clarity.
```
apiVersion: v1
  kind: Pod
  metadata:
    ---TRUNCATED---
    name: event-exporter-gke-564fb97f9-6bt5p
    namespace: kube-system
    --TRUNCATED---
  spec:
    containers:
    - image: gke.gcr.io/prometheus-to-sd:v0.10.0-gke.0
      name: prometheus-to-sd-exporter
      ---TRUNCATED---
  status:
    ---TRUNCATED---
```

Note that spec.containers is a List and each list item i.e. container would have a name and image. 
So the mapping for those names and images in our Pod manifest would be spec.containers[].name and 
spec.containers[].image respectively.

We are now going to get the details discussed above for each Pod.

```
for item in pod_list['items']:
    print(item.keys())
    pod_name = item['metadata']['name']
    pod_namespace = item['metadata']['namespace']
    container_list = item['spec']['containers']
    for container in container_list:
        container_name = container['name']
        container_image = container['image']
        file.write(f'{pod_name}\t{pod_namespace}\t{container_name}\t{container_image}\n')
```

The file should contain the details that we need.
```
$ head /tmp/container-img-inventory.csv 
Pod Name	Pod Namespace	Container Name	Container Image
event-exporter-gke-564fb97f9-6bt5p	kube-system	event-exporter	gke.gcr.io/event-exporter:v0.3.4-gke.0
event-exporter-gke-564fb97f9-6bt5p	kube-system	prometheus-to-sd-exporter	gke.gcr.io/prometheus-to-sd:v0.10.0-gke.0
fluentbit-gke-2mfvq	kube-system	fluentbit	gke.gcr.io/fluent-bit:v1.3.11-gke.0
fluentbit-gke-2mfvq	kube-system	fluentbit-gke	gke.gcr.io/fluent-bit-gke-exporter:v0.11.4-gke.0
fluentbit-gke-s5cjj	kube-system	fluentbit	gke.gcr.io/fluent-bit:v1.3.11-gke.0
fluentbit-gke-s5cjj	kube-system	fluentbit-gke	gke.gcr.io/fluent-bit-gke-exporter:v0.11.4-gke.0
fluentbit-gke-xxpgg	kube-system	fluentbit	gke.gcr.io/fluent-bit:v1.3.11-gke.0
fluentbit-gke-xxpgg	kube-system	fluentbit-gke	gke.gcr.io/fluent-bit-gke-exporter:v0.11.4-gke.0
gke-metrics-agent-9q24j	kube-system	gke-metrics-agent	gke.gcr.io/gke-metrics-agent:0.2.1-gke.0
```

Since the file is in csv format, we could use utilities like Excel or Google sheets to view the 
content in a graphical way.

---end-of-post---
    












