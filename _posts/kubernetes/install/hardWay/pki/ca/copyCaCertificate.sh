for i in {0..2}; do
    gcloud compute scp ca-k8s.pem master-${i}:/tmp
    gcloud compute ssh master-${i} -- sudo mv /tmp/ca-k8s.pem /etc/kubernetes/pki
done

for i in {0..4}; do
    gcloud compute scp ca-k8s.pem node-${i}:/tmp
    gcloud compute ssh node-${i} -- sudo mv /tmp/ca-k8s.pem /etc/kubernetes/pki
done
