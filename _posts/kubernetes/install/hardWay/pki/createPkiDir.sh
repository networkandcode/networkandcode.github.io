for i in {0..2}; do
gcloud compute ssh master-${i} -- sudo mkdir -p /etc/kubernetes/pki
done
for i in {0..4}; do
gcloud compute ssh node-${i} -- sudo mkdir -p /etc/kubernetes/pki
done
