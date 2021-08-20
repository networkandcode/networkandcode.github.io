---
title: kubernetes > bootstrap a cluster with rke
categories: kubernetes
...

Rancher Kubernetes Engine ( RKE ) is a popular tool using which we can bootstrap kubernetes clusters 
quickly. We are going to excatly see that in this post. Please ensure kubectl is installed in your 
system so that you can interact with the cluster after its launched. And You should be aware of the 
ssh key generation process.

We are going to perform this setup on a 3 node cluster comprising of 1 master and 2 worker nodes. 
The master node is our control plane node, that would also have etcd in it.

I have launched 3 * 4 GB Ubuntu 21.04 nodes on Linode cloud for this purpose. You can launch the VMs 
anywhere though. Here are the screenshots of the settings I have chosen while launching a node.
![Linode Node Creation](/assets/kubernetes-bootstrap-a-cluster-with-rke-1.png)
![Linode Node Creation](/assets/kubernetes-bootstrap-a-cluster-with-rke-2.png)
![Linode Node Creation](/assets/kubernetes-bootstrap-a-cluster-with-rke-3.png)
![Linode Node Creation](/assets/kubernetes-bootstrap-a-cluster-with-rke-4.png)

Once the nodes have started up, please make a note of their IPs (private and public)

Alright, lets generate cluster.yml, which would be the config for rke. The complete config would look 
like the following.
```
$ cat cluster.yml 
# If you intened to deploy Kubernetes in an air-gapped environment,
# please consult the documentation on how to configure custom RKE images.
nodes:
- address: <public ip of master>
  port: "22"
  internal_address: <private ip of master>
  role:
  - controlplane
  - etcd
  hostname_override: master
  user: root
  docker_socket: /var/run/docker.sock
  ssh_key: ""
  ssh_key_path: ~/.ssh/id_rsa
  ssh_cert: ""
  ssh_cert_path: ""
  labels: {}
  taints: []
- address: <public ip of node1>
  port: "22"
  internal_address: <private ip of node1>
  role:
  - worker
  hostname_override: node1
  user: root
  docker_socket: /var/run/docker.sock
  ssh_key: ""
  ssh_key_path: ~/.ssh/id_rsa
  ssh_cert: ""
  ssh_cert_path: ""
  labels: {}
  taints: []
- address: <public ip of node2>
  port: "22"
  internal_address: <private ip of node2>
  role:
  - worker
  hostname_override: node2
  user: root
  docker_socket: /var/run/docker.sock
  ssh_key: ""
  ssh_key_path: ~/.ssh/id_rsa
  ssh_cert: ""
  ssh_cert_path: ""
  labels: {}
  taints: []
services:
  etcd:
    image: ""
    extra_args: {}
    extra_binds: []
    extra_env: []
    win_extra_args: {}
    win_extra_binds: []
    win_extra_env: []
    external_urls: []
    ca_cert: ""
    cert: ""
    key: ""
    path: ""
    uid: 0
    gid: 0
    snapshot: null
    retention: ""
    creation: ""
    backup_config: null
  kube-api:
    image: ""
    extra_args: {}
    extra_binds: []
    extra_env: []
    win_extra_args: {}
    win_extra_binds: []
    win_extra_env: []
    service_cluster_ip_range: 10.43.0.0/16
    service_node_port_range: ""
    pod_security_policy: false
    always_pull_images: false
    secrets_encryption_config: null
    audit_log: null
    admission_configuration: null
    event_rate_limit: null
  kube-controller:
    image: ""
    extra_args: {}
    extra_binds: []
    extra_env: []
    win_extra_args: {}
    win_extra_binds: []
    win_extra_env: []
    cluster_cidr: 10.42.0.0/16
    service_cluster_ip_range: 10.43.0.0/16
  scheduler:
    image: ""
    extra_args: {}
    extra_binds: []
    extra_env: []
    win_extra_args: {}
    win_extra_binds: []
    win_extra_env: []
  kubelet:
    image: ""
    extra_args: {}
    extra_binds: []
    extra_env: []
    win_extra_args: {}
    win_extra_binds: []
    win_extra_env: []
    cluster_domain: cluster.local
    infra_container_image: ""
    cluster_dns_server: 10.43.0.10
    fail_swap_on: false
    generate_serving_certificate: false
  kubeproxy:
    image: ""
    extra_args: {}
    extra_binds: []
    extra_env: []
    win_extra_args: {}
    win_extra_binds: []
    win_extra_env: []
network:
  plugin: canal
  options: {}
  mtu: 0
  node_selector: {}
  update_strategy: null
  tolerations: []
authentication:
  strategy: x509
  sans: []
  webhook: null
addons: ""
addons_include: []
system_images:
  etcd: rancher/coreos-etcd:v3.4.15-rancher1
  alpine: rancher/rke-tools:v0.1.75
  nginx_proxy: rancher/rke-tools:v0.1.75
  cert_downloader: rancher/rke-tools:v0.1.75
  kubernetes_services_sidecar: rancher/rke-tools:v0.1.75
  kubedns: rancher/k8s-dns-kube-dns:1.15.2
  dnsmasq: rancher/k8s-dns-dnsmasq-nanny:1.15.2
  kubedns_sidecar: rancher/k8s-dns-sidecar:1.15.2
  kubedns_autoscaler: rancher/cluster-proportional-autoscaler:1.7.1
  coredns: rancher/coredns-coredns:1.6.9
  coredns_autoscaler: rancher/cluster-proportional-autoscaler:1.7.1
  nodelocal: rancher/k8s-dns-node-cache:1.15.7
  kubernetes: rancher/hyperkube:v1.18.20-rancher1
  flannel: rancher/coreos-flannel:v0.12.0
  flannel_cni: rancher/flannel-cni:v0.3.0-rancher6
  calico_node: rancher/calico-node:v3.13.4
  calico_cni: rancher/calico-cni:v3.13.4
  calico_controllers: rancher/calico-kube-controllers:v3.13.4
  calico_ctl: rancher/calico-ctl:v3.13.4
  calico_flexvol: rancher/calico-pod2daemon-flexvol:v3.13.4
  canal_node: rancher/calico-node:v3.13.4
  canal_cni: rancher/calico-cni:v3.13.4
  canal_flannel: rancher/coreos-flannel:v0.12.0
  canal_flexvol: rancher/calico-pod2daemon-flexvol:v3.13.4
  weave_node: weaveworks/weave-kube:2.6.4
  weave_cni: weaveworks/weave-npc:2.6.4
  pod_infra_container: rancher/pause:3.1
  ingress: rancher/nginx-ingress-controller:nginx-0.35.0-rancher2
  ingress_backend: rancher/nginx-ingress-controller-defaultbackend:1.5-rancher1
  metrics_server: rancher/metrics-server:v0.3.6
  windows_pod_infra_container: rancher/kubelet-pause:v0.1.6
ssh_key_path: ~/.ssh/id_rsa
ssh_cert_path: ""
ssh_agent_auth: false
authorization:
  mode: rbac
  options: {}
ignore_docker_version: null
kubernetes_version: ""
private_registries: []
ingress:
  provider: ""
  options: {}
  node_selector: {}
  extra_args: {}
  dns_policy: ""
  extra_envs: []
  extra_volumes: []
  extra_volume_mounts: []
  update_strategy: null
  http_port: 0
  https_port: 0
  network_mode: ""
  tolerations: []
cluster_name: ""
cloud_provider:
  name: ""
prefix_path: ""
win_prefix_path: ""
addon_job_timeout: 0
bastion_host:
  address: ""
  port: ""
  user: ""
  ssh_key: ""
  ssh_key_path: ""
  ssh_cert: ""
  ssh_cert_path: ""
monitoring:
  provider: ""
  options: {}
  node_selector: {}
  update_strategy: null
  replicas: null
  tolerations: []
restore:
  restore: false
  snapshot_name: ""
dns: null
```

Just replace the public and private IPs of nodes in this file and you are good to go. If you want more 
customization, you can also generate this config using the rke step by step prompt by saying 
```rke config --name cluster.yml```.

Please ensure docker is installed on all three nodes. You just need to ssh in to each node, and run 
``` apt update -y && apt install docker.io -y ```. Use sudo if required.

Fine, let's now go ahead and lauch the cluster.
```
networkandcode@ubuntu20:~$ rke up
INFO[0000] Running RKE version: v1.1.19                 
INFO[0000] Initiating Kubernetes cluster                
INFO[0000] [certificates] GenerateServingCertificate is disabled, checking if there are unused kubelet certificates 
INFO[0000] [certificates] Generating admin certificates and kubeconfig 
INFO[0000] Successfully Deployed state file at [./cluster.rkestate] 
INFO[0000] Building Kubernetes cluster                  
---TRUNCATED---
NFO[0190] [addons] Executing deploy job rke-ingress-controller 
INFO[0191] [ingress] ingress controller nginx deployed successfully 
INFO[0191] [addons] Setting up user addons              
INFO[0191] [addons] no user addons defined              
INFO[0191] Finished building Kubernetes cluster successfully 
```

The cluster is ready, you can copy the kubeconfig as follows.
```
$ mkdir .kube
$ touch .kube/config

$ cp kube_config_cluster.yml .kube/config
```

Thats it, you should see the nodes with kubectl.
```
networkandcode@ubuntu20:~$ kubectl config current-context
local

networkandcode@ubuntu20:~$ kubectl get nodes
NAME     STATUS   ROLES               AGE     VERSION
master   Ready    controlplane,etcd   16h     v1.18.20
node1    Ready    worker              6m20s   v1.18.20
node2    Ready    worker              7m27s   v1.18.20
```

So as we saw, creating a cluster with RKE is quick, and we can apply this concept to VMs on cloud or 
on premises.

Thats the end of the post, Thank you for reading...

--end-of-post--
