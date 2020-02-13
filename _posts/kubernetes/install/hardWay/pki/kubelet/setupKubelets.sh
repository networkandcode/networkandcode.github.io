for i in {0..4}; do

ext_ip=$(gcloud compute instances describe node-${i} \
  --format 'value(networkInterfaces[0].accessConfigs[0].natIP)')

int_ip=$(gcloud compute instances describe node-${i} \
  --format 'value(networkInterfaces[0].networkIP)')
  
cfssl gencert \
    -ca ../ca/ca-k8s.pem \
    -ca-key ../ca/ca-k8s-key.pem \
    -config ../ca/ca-config.json \
    -profile k8s-profile \
    -hostname ${i},${ext_ip},${int_ip} \
    kubelet-${i}-csr.json | cfssljson -bare kubelet-${i}

done
