for i in {0..2}; do
    gcloud compute scp service-account.pem service-account-key.pem master-${i}:/tmp/
    gcloud compute ssh master-${i} -- sudo mv /tmp/service-account* /etc/kubernetes/pki/
done
