We could create Pod volumes based on Secrets and mount those into containers. It's good to have some understanding of Secrets and Volumes to make most use of this post.

Let's define manifests for a secret and a pod as follows.

```
networkandcode: $ cat secret-sample.yaml
---
apiVersion:  v1
kind: secret
metadata:
  name: secret-sample
data:
  animal: elephant
  bird: parrot
  car: jaguar
...  

networkandcode: $ cat pod-sample.yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-sample
spec:
  volumes:
  - name: volume1
    secret:
      secretName: secret-sample
  containers:
  - name: apache
    image: httpd
    volumeMounts:
    - name: volume1
      mountPath: /tmp/apache
...
```

The secret and pod could now be created
```
networkandcode: $ kubectl create -f secret-sample.yaml
secret/secret-sample created

networkandcode: $ kubectl create -f pod-sample.yaml
pod/pod-sample created
```

The secret data gets imported to the container inside the pod, as files in the mount path, one file for a key

```
networkandcode: $ kubectl exec -it pod-sample -- ls /tmp/apache
animal  bird  car
```

The contents of these files would have the values of the data keys, as defined in the secret's manifest

```
networkandcode: $ kubectl exec -it pod-sample -- cat /tmp/apache/animal ; echo
elephant

networkandcode: $ kubectl exec -it pod-sample -- cat /tmp/apache/bird ; echo
parrot

networkandcode: $ kubectl exec -it pod-sample -- cat /tmp/apache/car ; echo
jaguar
```

Cleanup
```
networkandcode: $ kubectl delete secret secret-sample

networkandcode: $ kubectl delete pod pod-sample
```

--end-of-post--
