for i in 0 1 2; do
    gcloud compute instances create master-     --image-family ubuntu-1804-lts     --image-project ubuntu-os-cloud
done
