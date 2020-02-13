ext_ip=$(gcloud compute addresses describe kube-apiserver \
  --region $(gcloud config get-value compute/region) \
  --format 'value(address)')

int_ip_0=$(gcloud compute instances describe master-0 \
        --format 'value(networkInterfaces[0].networkIP)')
int_ip_1=$(gcloud compute instances describe master-1 \
        --format 'value(networkInterfaces[0].networkIP)')
int_ip_2=$(gcloud compute instances describe master-2 \
        --format 'value(networkInterfaces[0].networkIP)')


cfssl gencert \
  -ca=../ca/ca-k8s.pem \
  -ca-key=../ca/ca-k8s-key.pem \
  -config=../ca/ca-config.json \
  -hostname=${int_ip_0},${int_ip_1},${int_ip_2},127.0.0.1,kubernetes.default \
  -profile=k8s-profile \
  kube-apiserver-csr.json | cfssljson -bare kube-apiserver
