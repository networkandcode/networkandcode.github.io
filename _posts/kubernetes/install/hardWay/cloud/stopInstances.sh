for i in {0..2}; do
    gcloud compute instances stop master-${i}
done

for i in {0..4}; do
    gcloud compute instances stop node-${i}
done
