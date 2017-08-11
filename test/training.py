#!/usr/bin/python

# Copyright 2013-present Barefoot Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from scapy.all import *
import sys, time
import random, string, threading

total_rec=0
quota_arr=[40,60,40,60]
PKTS_NUM=random.randint(30,150)
slat=random.randint(70,230)/1000
DIP_NUM=4
INTF="veth2"
time1=0

def cpu_ans(k):
    with open("temp_cpu%s"%(k,),"r") as f:
        data=f.read()
    p=re.compile(r"[0-9]+.[0-9]+%")
    m=p.findall(data)
    res1=[float(m[2*i][:-2]) for i in range(len(m)//6)]
    res2=[float(m[2*i][:-2]) for i in range(len(m)//6,len(m)//3)]
    res3=[float(m[2*i][:-2]) for i in range(len(m)//3,len(m)//2)]
    quota=quota_arr[k-1]
    return "%f %f %f "%(sum(res1)/len(res1)/quota,sum(res2)/len(res2)/quota,sum(res3)/len(res3)/quota)

def get_pkts(index):
  p=re.compile("packets=[0-9]+")
  a=os.popen("/home/wsb/bmv2/targets/simple_switch/sswitch_CLI LBswitch.json < pkt_commands")
  m=p.findall(a.read())
  return m[index].split("=")[-1]

def send_random_traffic():
    global time1
    random_ports = random.sample(range(1024,65535), PKTS_NUM-1)
    total_pkts = 0
    src_mac="00:00:07:23:07:23"
    dst_mac="00:00:00:00:07:23"
    dst_ip="7.23.7.23"
    src_ip="10.0.7.23"
    for port in random_ports:
        p = Ether(dst=dst_mac,src=src_mac)/IP(dst=dst_ip,src=src_ip)
        p = p/TCP(dport=port)/Raw(load="normal")
        sendp(p, iface = INTF)
        total_pkts += 1
        time.sleep(slat)
    p = Ether(dst=dst_mac,src=src_mac)/IP(dst=dst_ip,src=src_ip)
    p = p/TCP(dport=port)/Raw(load="end")
    sendp(p, iface = INTF)
    time1=time.time()
    
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
            data = pkt[Raw].load
            print ("Received from %s, %s" %(id_tup,data))
            total_rec+=1
            if(data!=b"normal"):
                time2=time.time()-time1
                data=int(data)
                with open("data%d"%(quota_arr[data-1]),'a') as f :
                    f.write(cpu_ans(data))
                    f.write("%s "%(get_pkts(data-1),))
                    f.write("%d "%(quota_arr[data-1],))
                    f.write("%f\n"%(time2,))
            if(total_rec==PKTS_NUM):
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

