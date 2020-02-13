source getInstances.sh

stop () {
    gcloud compute instances stop $1 --quiet
}

for i in "${instances[@]}"; do
    stop $i &
done

wait

echo done
