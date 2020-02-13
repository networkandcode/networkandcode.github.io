source getInstances.sh

start () {
    gcloud compute instances start $1
    if [ $? != 0 ]
    then
      echo "Creating ${1} as it doesn't exist"
      if [[ $1 == *"master"* ]]
      then
          custom="--custom-cpu 2 --custom-memory 4"
      else
          custom=""
      fi
      gcloud compute instances create $1 --image-family ubuntu-1804-lts --image-project ubuntu-os-cloud $custom
      #--custom-cpu 2 --custom-memory 4
    fi
}

for i in "${instances[@]}"; do
    start $i &
done

wait

echo done
