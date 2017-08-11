from scapy.all import *
import sys, time, weight, os
import random, string, threading

total_rec=0
quota_arr=[40,60,40,60]
PKTS_NUM=200
WHEN_UPDATE=120
slat=0.1
times=[0 for i in range(PKTS_NUM)]
DIP_NUM=4
INTF="veth2"
time1=0
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
                with open("cpu_usage_ecmp",'a') as f:
                    f.write("%d %f\n"%(1,weight.cpu_ans(1)))
                    f.write("%d %f\n"%(2,weight.cpu_ans(2)))
                    f.write("%d %f\n"%(3,weight.cpu_ans(3)))
                    f.write("%d %f\n"%(4,weight.cpu_ans(4)))
                for i in range(4):
                    os.system("cp temp_cpu%d cpu_record_ecmp%d"%(i+1,i+1))
                exit(0)
                

if __name__ == '__main__':
    t1=threading.Thread(target=send_random_traffic)
    t1.start()
    ts=[threading.Thread(target=os.system, args=("docker stats h%s > temp_cpu%s"%(i+1,i+1),)) for i in range(DIP_NUM)]
    for t in ts:
        t.setDaemon(True)
        t.start()


    sniff(iface = INTF,
          prn = lambda x: handle_pkt(x))

