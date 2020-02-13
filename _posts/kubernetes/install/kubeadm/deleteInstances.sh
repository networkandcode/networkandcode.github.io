source getInstances.sh

delete () {
    gcloud compute instances delete $1 --quiet
}

for i in "${instances[@]}"; do
    delete $i &
done

wait

echo done
