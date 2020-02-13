for i in {0..4}; do
    gcloud compute scp kubelet-${i}.pem kubelet-${i}-key.pem node-${i}:/tmp/
    gcloud compute ssh node-${i} -- sudo mv /tmp/kubelet-${i}.pem /etc/kubernetes/pki/
done
