HOST_NUM=5

mkdir -p /var/run/netns
./veth_setup.sh

quota_arr=(60000 40000 60000 40000 60000 40000 60000 40000 60000 40000)
cpuset_arr=(0 1 2 3 4 5 6 0 7 0)

idx=1

while [ $idx -lt $HOST_NUM ]
do
    intf="veth$(($idx*2+3))"
    hostname="h$idx"
    docker run -t -i -u root -d --rm --name=$hostname --net=none --cpu-period=100000 --cpu-quota=${quota_arr[$idx]} --cpuset-cpus=${cpuset_arr[$idx]} scapy
    docker cp docker.py $hostname:.
    PID=$(docker inspect -f '{{.State.Pid}}' $hostname)
    ln -s /proc/$PID/ns/net /var/run/netns/$PID
    ip link set $intf netns $PID
    ip netns exec $PID ip link set dev $intf name eth0 
    ip netns exec $PID ip link set eth0 up 
    ip netns exec $PID ip addr add 10.10.10.$idx/24 dev eth0
    xterm -T $hostname -hold -e docker exec -it $hostname python3 docker.py $idx &
    idx=$((idx + 1))
done
