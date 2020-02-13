# Appendix - Calico Installation and Verification

## To Install Calico networking agents on all the Instances
```kubectl apply -f https://docs.projectcalico.org/v3.10/manifests/calico.yaml```

## To Install Calico controller
```
networkandcode@k8s-master-0:~$ kubectl apply -f https://docs.projectcalico.org/v3.10/manifests/calicoctl.yaml
serviceaccount/calicoctl created
pod/calicoctl created
clusterrole.rbac.authorization.k8s.io/calicoctl created
clusterrolebinding.rbac.authorization.k8s.io/calicoctl created
```

## To Check the profiles
```
networkandcode@k8s-master-0:~$ kubectl exec -it calicoctl -n kube-system -- /calicoctl get profiles -o wide
NAME                                                 LABELS   
kns.default                                                   
kns.kube-node-lease                                           
kns.kube-public                                               
kns.kube-system                                               
ksa.default.default                                           
ksa.kube-node-lease.default                                   
ksa.kube-public.default                                       
ksa.kube-system.attachdetach-controller                       
ksa.kube-system.bootstrap-signer                              
ksa.kube-system.calico-kube-controllers                       
ksa.kube-system.calico-node                                   
ksa.kube-system.calicoctl                                     
ksa.kube-system.certificate-controller                        
ksa.kube-system.clusterrole-aggregation-controller            
ksa.kube-system.coredns                                       
ksa.kube-system.cronjob-controller                            
ksa.kube-system.daemon-set-controller                         
ksa.kube-system.default                                       
ksa.kube-system.deployment-controller                         
ksa.kube-system.disruption-controller                         
ksa.kube-system.endpoint-controller                           
ksa.kube-system.expand-controller                             
ksa.kube-system.generic-garbage-collector                     
ksa.kube-system.horizontal-pod-autoscaler                     
ksa.kube-system.job-controller                                
ksa.kube-system.kube-proxy                                    
ksa.kube-system.namespace-controller                          
ksa.kube-system.node-controller                               
ksa.kube-system.persistent-volume-binder                      
ksa.kube-system.pod-garbage-collector                         
ksa.kube-system.pv-protection-controller                      
ksa.kube-system.pvc-protection-controller                     
ksa.kube-system.replicaset-controller                         
ksa.kube-system.replication-controller                        
ksa.kube-system.resourcequota-controller                      
ksa.kube-system.service-account-controller                    
ksa.kube-system.service-controller                            
ksa.kube-system.statefulset-controller                        
ksa.kube-system.token-cleaner                                 
ksa.kube-system.ttl-controller
```

## To set an alias
```
networkandcode@k8s-master-0:~$ alias calicoctl="kubectl exec -i -n kube-system calicoctl /calicoctl -- "
```

## To check the list of nodes
```
networkandcode@k8s-master-0:~$ calicoctl get nodes
NAME           
k8s-master-0   
k8s-node-0     
k8s-node-1     
k8s-node-2
```
