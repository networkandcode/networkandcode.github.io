Create a file with the scripts for API objects creation
```
networkandcode@k8s-master-0:~$ cat launchDemo.sh <<EOF
kubectl create -f https://docs.projectcalico.org/v3.10/security/tutorials/kubernetes-policy-demo/manifests/00-namespace.yaml
kubectl create -f https://docs.projectcalico.org/v3.10/security/tutorials/kubernetes-policy-demo/manifests/01-management-ui.yaml
kubectl create -f https://docs.projectcalico.org/v3.10/security/tutorials/kubernetes-policy-demo/manifests/02-backend.yaml
kubectl create -f https://docs.projectcalico.org/v3.10/security/tutorials/kubernetes-policy-demo/manifests/03-frontend.yaml
kubectl create -f https://docs.projectcalico.org/v3.10/security/tutorials/kubernetes-policy-demo/manifests/04-client.yaml
EOF
```

Make the shell file executable
```
networkandcode@k8s-master-0:~$ chmod +x launchDemo.sh
```

Execute the script
```
networkandcode@k8s-master-0:~$ ./launchDemo.sh
```

Check the NodePort on which the management-ui is accessible
```
networkandcode@k8s-master-0:~$ kubectl get svc -n management-ui
NAME            TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
management-ui   NodePort   10.97.231.153   <none>        9001:30002/TCP   51s
```

Check the node on which the management-ui Pod is launched
```
networkandcode@k8s-master-0:~$ kubectl get po -o wide -n management-ui 
NAME                  READY   STATUS    RESTARTS   AGE     IP               NODE         NOMINATED NODE   READINESS GATES
management-ui-9z9pg   1/1     Running   0          5m35s   192.168.11.194   k8s-node-0   <none>           <none>
```


