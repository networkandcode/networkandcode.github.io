sudo su
mkdir -pm 777 /var/lib/contrail/kafka-logs
curl \
    https://raw.githubusercontent.com/Juniper/contrail-kubernetes-docs/master/install/kubernetes/templates/contrail-single-step-cni-install-ubuntu.yaml \
    | sed "s/{{ K8S_MASTER_IP }}/$K8S_MASTER_IP/g; s/{{ CONTRAIL_REPO }}/$CONTRAIL_REPO/g; s/{{ CONTRAIL_RELEASE }}/$CONTRAIL_RELEASE/g" \
    | kubectl apply -f -
