 for i in {0..2}; do
    gcloud compute scp kube-apiserver.pem kube-apiserver-key.pem master-${i}:/tmp/
    gcloud compute ssh master-${i} -- sudo mv /tmp/kube-apiserver* /etc/kubernetes/pki/
done
