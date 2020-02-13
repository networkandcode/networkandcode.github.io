source setVariables.sh
./setDefaults.sh

declare -a instances
declare -a masters
declare -a nodes

for (( i=0; i<${noOfMasters}; i++ )); do
    masters+=("${masterPrefix}-${i}")
    instances+=("${masterPrefix}-${i}")
done

for (( i=0; i<${noOfNodes}; i++ )); do
    nodes+=("${nodePrefix}-${i}")
    instances+=("${nodePrefix}-${i}")
done
