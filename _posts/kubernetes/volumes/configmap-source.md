We could create Pod volumes based on Config Maps and mount those into containers. It's good to have some understanding of Config Maps and Volumes to make most use of this post. 

Let's define manifests for a config map and a pod as follows. 

```
networkandcode: $ cat configmap-sample.yaml
---
apiVersion:  v1
kind: ConfigMap
metadata:
  name: configmap-sample
data:
  animal: lion
  bird: dove
  car: audi
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
    configMap:
      name: configmap-sample
  containers:
  - name: apache
    image: httpd
    volumeMounts:
    - name: volume1
      mountPath: /tmp/apache
...
```

The ConfigMap and Pod are going to be created
```
networkandcode: $ kubectl create -f configmap-sample.yaml
configmap/configmap-sample created

networkandcode: $ kubectl create -f pod-sample.yaml
pod/pod-sample created
```

The config map data gets imported to the container inside the pod, as files in the mount path, one file for a key
```
networkandcode: $ kubectl exec -it pod-sample -- ls /tmp/apache
animal  bird  car
```

The contents of these files would have the values of the data keys, as defined in the config map's manifest
```
networkandcode: $ kubectl exec -it pod-sample -- cat /tmp/apache/animal ; echo
lion

networkandcode: $ kubectl exec -it pod-sample -- cat /tmp/apache/bird ; echo
dove

networkandcode: $ kubectl exec -it pod-sample -- cat /tmp/apache/car ; echo
audi
```

Cleanup
```
networkandcode: $ kubectl delete cm configmap-sample

networkandcode: $ kubectl delete pod pod-sample
```

--end-of-post--
