echo 'Checking connection to masters'

for i in {0..2}; do
    exit | gcloud compute ssh master-
    echo 'connection successful to master-'
done

echo 'Checking connection to nodes'
for i in {0..4}; do
    exit | gcloud compute ssh node-
    echo 'connection successful to node-'
done
