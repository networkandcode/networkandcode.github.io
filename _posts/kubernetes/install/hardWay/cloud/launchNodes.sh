for i in {0..4}; do
    gcloud compute instances create node-     --image-family ubuntu-1804-lts     --image-project ubuntu-os-cloud     --metadata pod-cidr=192.168..0/24
done
