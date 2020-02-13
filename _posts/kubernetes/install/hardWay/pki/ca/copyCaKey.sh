for i in {0..2}; do
    gcloud compute scp ca-k8s-key.pem master-${i}:/tmp
    gcloud compute ssh master-${i} -- sudo mv /tmp/ca-k8s-key.pem /etc/kubernetes/pki
done
