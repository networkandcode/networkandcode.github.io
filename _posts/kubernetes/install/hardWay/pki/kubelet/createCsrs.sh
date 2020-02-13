for i in {0..4}; do
cat > kubelet-${i}-csr.json <<EOF
{
    "CN": "system:nodes:${i}",
    "key": {
        "algo": "ecdsa",
        "size": 256
    },
    "names": [
        {
            "C": "US",
            "ST": "CA",
            "L": "San Francisco",
            "O": "system:nodes",
            "OU": "k8s-hard-way"
        }
    ]
}
EOF
done
