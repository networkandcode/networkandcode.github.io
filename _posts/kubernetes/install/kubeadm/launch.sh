source setVariables.sh
source getInstances.sh

./startInstances.sh

execCommands() {
    cat $2 | gcloud compute ssh $1
}

installKube() {
    sudo su
    apt-get install -y $1
    apt-mark hold $1
}

for i in "${instances[@]}"; do
    for j in installDocker.sh addK8sRepos.sh installKubeadm.sh; do
        execCommands $i $j
    done &
done

wait

for i in "${nodes[@]}"; do
    execCommands $i installKubelet.sh &
done

wait

for i in "${masters[@]}"; do
    execCommands $i installKubectl.sh &
done

wait

for i in "${instances[@]}"; do
    execCommands $i resetCluster.sh &
done

wait

for i in "${masters[@]}"; do
    cat initCluster.sh | gcloud compute ssh $i > initOutput.sh
done

for i in "${masters[@]}"; do
    execCommands $i setupKubeconfig.sh &
done

if [ "$networkPlugin" == "calico" ]
then
    for i in "${masters[@]}"; do
        execCommands $i installCalico.sh 
    done
elif [ "$networkPlugin" == "tungsten" ]
then
    export K8S_MASTER_IP=${intMasterIp}
    export CONTRAIL_REPO="docker.io\/opencontrailnightly"
    export CONTRAIL_RELEASE="latest"
    cat installTungsten.sh | gcloud compute ssh master
fi

echo 'sudo su' > joinNodes.sh
cat initOutput.sh | tail -2 >> joinNodes.sh

for i in "${nodes[@]}"; do
    execCommands $i joinNodes.sh &
done

wait

echo '````````````````````````````````````````````````````'
echo 'Your cluster is ready, login to the master and enjoy'
