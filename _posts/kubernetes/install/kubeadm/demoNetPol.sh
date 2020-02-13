source getInstances.sh
declare -a manifests=( "ex25-deploy.yaml" "ex25-svc-ci.yaml" "ex25-po-apache.yaml" )

for i in "${masters[@]}"
do
    gcloud compute scp ../../ex25* $i:~
    for j in "${manifests[@]}"
    do
        gcloud compute ssh $i -- kubectl create -f $j
    done
    #gcloud compute ssh $i -- "kubectl exec -it po25-apache -- echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf > /dev/null"
    #gcloud compute ssh $i -- apt update -y
    #gcloud compute ssh $i -- apt install curl -y
done
