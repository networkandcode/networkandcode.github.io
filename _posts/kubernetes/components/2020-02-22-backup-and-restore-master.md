---
title: kubernetes > backup and restore the master
categories: kubernetes
---

This post covers information about how to backup and restore a Kubernetes master. The prerequisite is to have knowledge of launching a cluster using kubeadm.

Backing up a master involves backing up the etcd server and backing up TLS certificates of the cluster components

On a typical cluster bootstrapped with kubeadm, we could find all the TLS certificates at the following path of the master

```
networkandcode@master $ ls /etc/kubernetes/pki
apiserver.crt              apiserver-kubelet-client.crt  etcd                    front-proxy-client.key
apiserver-etcd-client.crt  apiserver-kubelet-client.key  front-proxy-ca.crt      sa.key
apiserver-etcd-client.key  ca.crt                        front-proxy-ca.key      sa.pub
apiserver.key              ca.key                        front-proxy-client.crt
```

And there is a seperate sub directory for the etcd TLS certificates
```
networkandcode@master $ ls /etc/kubernetes/pki/etcd
ca.crt  ca.key  healthcheck-client.crt  healthcheck-client.key  peer.crt  peer.key  server.crt  server.key
```

Let's create a directory for backing up these certificates, and then move these certificates there
```
networkandcode@master $ mkdir backup-k8s-tls-certs
networkandcode@master $ cp -r /etc/kubernetes/pki backup-k8s-tls-certs/
networkandcode@master $ ls backup-k8s-tls-certs/
pki
```

Now let's create a separate directory for backing up etcd
```
networkandcode@master $ mkdir backup-etcd
```

We need to install the etcdctl tool to backup etcd easily, we can do it using the go language
```
# install etcdctl
networkandcode@master$ go get github.com/coreos/etcd/etcdctl
```

We may now backup the etcd server, using etcdctl
```
networkandcode@master $ ETCDCTL_API=3 \ 
  etcdctl snapshot save backup-etcd/snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt \
  --key=/etc/kubernetes/pki/etcd/healthcheck-client.key

{"level":"info","ts":1582355056.9277308,"caller":"snapshot/v3_snapshot.go:110","msg":"created temporary dbfile","path":"backup-etcd/snapshot.db.part"}
{"level":"info","ts":1582355056.9408722,"caller":"snapshot/v3_snapshot.go:121","msg":"fetching snapshot","endpoint":"127.0.0.1:2379"}
{"level":"info","ts":1582355057.017826,"caller":"snapshot/v3_snapshot.go:134","msg":"fetched snapshot","endpoint":"127.0.0.1:2379","took":0.09000424}
{"level":"info","ts":1582355057.0179946,"caller":"snapshot/v3_snapshot.go:143","msg":"saved","path":"backup-etcd/snapshot.db"}
Snapshot saved at backup-etcd/snapshot.db

networkandcode@master $ ls backup-etcd -ltr
total 2592
-rw------- 1 root root 2650144 Feb 22 08:49 snapshot.db

```

In the command above, we are first setting the ETCDCTL_API as version 3, then we are saving the server's snapshot at the mentioned path. The endpoints 
parameter refers to the address and port of the etcd server. 

We also need to add three extra parameters which source relevant ETCD certificates from the respective paths

The snapshot is now saved. So by now we have the backup of the cluster TLS certificates and the ETCD server

We are now going to simulate resetting the master
```
networkandcode@master$ kubeadm reset -f
```

The kubectl commands wouldnt now work as before
```
networkandcode@master $ kubectl get nodes
The connection to the server 172.16.0.17:6443 was refused - did you specify the right host or port?
```

The pki directory would be empty
```
networkandcode@master $ ls /etc/kubernetes/pki
networkandcode@master $
```

We may now copy the PKI certificates from the backup directory
```
networkandcode@master $ cp -r backup-k8s-tls-certs/pki /etc/kubernetes/

networkandcode@master $ ls /etc/kubernetes/pki
apiserver.crt              apiserver.key                 ca.crt  front-proxy-ca.crt      front-proxy-client.key
apiserver-etcd-client.crt  apiserver-kubelet-client.crt  ca.key  front-proxy-ca.key      sa.key
apiserver-etcd-client.key  apiserver-kubelet-client.key  etcd    front-proxy-client.crt  sa.pub
```

We may now restore etcd
```
networkandcode@master $ ETCDCTL_API=3 \
  etcdctl snapshot restore backup-etcd/snapshot.db
{"level":"info","ts":1582365349.7406623,"caller":"snapshot/v3_snapshot.go:287","msg":"restoring snapshot","path":"backup-etcd/snapshot.db","wal-dir":"default.etcd/member/wal","data-dir":"default.etcd","snap-dir":"default.etcd/member/snap"}
{"level":"info","ts":1582365349.82723,"caller":"membership/cluster.go:375","msg":"added member","cluster-id":"cdf818194e3a8c32","local-member-id":"0","added-peer-id":"8e9e05c52164694d","added-peer-peer-urls":["http://localhost:2380"]}
{"level":"info","ts":1582365349.8592656,"caller":"snapshot/v3_snapshot.go:300","msg":"restored snapshot","path":"backup-etcd/snapshot.db","wal-dir":"default.etcd/member/wal","data-dir":"default.etcd","snap-dir":"default.etcd/member/snap"}
```

The command above should have created the following files
```
networkandcode@master $ tree default.etcd/
default.etcd/
└ member
    ├ snap
    │   ├ 0000000000000001-0000000000000001.snap
    │   └ db
    └ wal
        └ 0000000000000000-0000000000000000.wal

3 directories, 3 files
```

We may move these files to a different directory, so that kubeadm would use this for the etcd server it creates
```
networkandcode@master $ mv default.etcd/member /var/lib/etcd/
networkandcode@master $ tree /var/lib/etcd
/var/lib/etcd
└ member
    ├ snap
    │   ├ 0000000000000001-0000000000000001.snap
    │   └ db
    └ wal
        └ 0000000000000000-0000000000000000.wal

3 directories, 3 files
```

The cluster could be bootstrapped again using kubeadm, however we need to include a flag to indicate it would use the existing data for etcd
```
networkandcode@master $ kubeadm init --ignore-preflight-errors=DirAvailable--var-lib-etcd
```

The master is recovered and it shows the nodes again
```
master $ kubectl get no
NAME     STATUS   ROLES    AGE   VERSION
master   Ready    master   33m   v1.14.0
node01   Ready    <none>   31m   v1.14.0
```

So we recovered the master, and when we initialized it using kubeadm, we didnt have to join the node to the cluster using kubeadm join

--end-of-post--
