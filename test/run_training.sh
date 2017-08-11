idx=1
round=10000
while [ $idx -lt $round ]
do
    python3 training.py
    rm temp_cpu*
done
