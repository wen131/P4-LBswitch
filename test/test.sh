round=2

idx=1
while [ $idx -lt $round ]
do
    rm temp_cpu*
    /home/wsb/bmv2/targets/simple_switch/sswitch_CLI LBswitch.json < reset_command
    python3 time_servers_weight.py
    idx=$((idx + 1))
done


rm temp_cpu*
