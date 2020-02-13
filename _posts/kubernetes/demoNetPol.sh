source install/kubeadm/getInstances.sh

for i in "${masters[@]}"; do
    gcloud compute ssh $i -- kubectl create -f ex25-deploy.yaml
    gcloud compute ssh $i -- kubectl create -f ex25-svc-ci.yaml    
    gcloud compute ssh $i -- kubectl create -f ex25-po-apache.yaml
done

echo done

