gcloud config set compute/region us-central1
gcloud config set compute/zone  us-central1-a

gcloud compute instances create master --image-family ubuntu-1804-lts --image-project ubuntu-os-cloud --custom-cpu 2 --custom-memory 4

for i in {0..2}; do
    gcloud compute instances create node-${i} --image-family ubuntu-1804-lts --image-project ubuntu-os-cloud
done

for i in master node-0 node-1 node-2; do
    cat installDocker.sh | gcloud compute ssh ${i}
    gcloud compute ssh ${i} -- sudo usermod -aG docker $USER
    cat addK8sRepos.sh | gcloud compute ssh ${i}
    cat installKubeadm.sh | gcloud compute ssh ${i}
done

for i in {0..2}; do
    cat installKubelet.sh | gcloud compute ssh node-${i}
done

cat installKubectl.sh | gcloud compute ssh master
cat initCluster.sh | gcloud compute ssh master > joinNodes.sh
cat setupKubeconfig.sh | gcloud compute ssh master
cat podNetworking.sh | gcloud compute ssh master

