for i in {0..2}; do
    gcloud compute instances start master-${i}
done

for i in {0..4}; do
    gcloud compute instances start node-${i}
done
