round=50

idx=1
while [ $idx -lt $round ]
do
    rm temp_cpu*
    python3 time_servers_ecmp.py
    idx=$((idx + 1))
done

idx=1
while [ $idx -lt $round ]
do
    rm temp_cpu*
    /home/wsb/bmv2/targets/simple_switch/sswitch_CLI LBswitch.json < reset_command
    python3 time_servers_static.py
    idx=$((idx + 1))
done

idx=1
while [ $idx -lt $round ]
do
    rm temp_cpu*
    /home/wsb/bmv2/targets/simple_switch/sswitch_CLI LBswitch.json < reset_command
    python3 time_servers_weight.py
    idx=$((idx + 1))
done


rm temp_cpu*