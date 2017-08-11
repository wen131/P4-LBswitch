from scapy.all import *
import sys, time, weight
import random, string, threading

total_rec=0
quota_arr=[40,60,40,60,40,60]
PKTS_NUM=200
WHEN_UPDATE=120
times=[0]*PKTS_NUM
DIP_NUM=6
INTF="veth2"
CLI_PATH='/home/wsb/bmv2/targets/simple_switch/sswitch_CLI LBswitch.json'


def send_random_traffic():
    random_ports = random.sample(range(1024,65535), PKTS_NUM)
    total_pkts = 0
    src_mac="00:00:07:23:07:23"
    dst_mac="00:00:00:00:07:23"
    dst_ip="7.23.7.23"
    src_ip="10.0.7.23"
    for port in random_ports:
        p = Ether(dst=dst_mac,src=src_mac)/IP(dst=dst_ip,src=src_ip)
        p = p/TCP(dport=port)/Raw(load=str(total_pkts))
        sendp(p, iface = INTF)
        times[total_pkts]=time.time()
        total_pkts += 1
    
def handle_pkt(pkt):
    global total_rec
    if IP in pkt and TCP in pkt:
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        proto = pkt[IP].proto
        sport = pkt[TCP].sport
        dport = pkt[TCP].dport
        if(src_ip=="7.23.7.23"):
            id_tup = (src_ip, dst_ip, proto, sport, dport)
            data = int(pkt[Raw].load)
            times[data]= time.time() - times[data]
            print ("Received from %s, %d" %(id_tup,data))
            total_rec+=1
            
            if(total_rec==PKTS_NUM):
                with open("time_sstatic9",'a') as f:
                    f.write("%f\n"%(sum(times),))
                exit(0)

if __name__ == '__main__':
    t1=threading.Thread(target=send_random_traffic)
    t1.start()

    sniff(iface = INTF,
          prn = lambda x: handle_pkt(x))

