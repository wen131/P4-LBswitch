from scapy.all import *
import sys, time, weight_cpu
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

def update():
    args=weight_cpu.get_args(True)
    i=0
    with open('temp_commands.txt','w') as f:
        for arg in args:
            f.write('table_add route_table select_dip %d %d => %d\n'%(i,1,arg))
            i+=1
        f.write('register_write version_register 0 %d\n'%(1,))
        f.write('counter_reset request_counter\n')
    os.system('%s < %s'%(CLI_PATH, 'temp_commands.txt'))


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
        if total_pkts == WHEN_UPDATE:
            update()
        time.sleep(slat)
    
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
                with open("time_cpu_weight_50",'a') as f:
                    f.write("%f\n"%(sum(times),))
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

