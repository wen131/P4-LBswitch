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
import sys
import random, string, threading
import weight

total_rec=0
PKTS_NUM=200
WHEN_UPDATE=100
INTF="veth2"
CLI_PATH='/home/wsb/bmv2/targets/simple_switch/sswitch_CLI LBswitch.json'

def update():
    args=[0,0,0,0,1,1,1,1,1,1,2,2,2,2,3,3,3,3,3,3,0,0,1,1,1,2,2,3,3,3,1,3]
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
        total_pkts += 1
        if(total_pkts==WHEN_UPDATE):
            update()

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
            if(total_rec==PKTS_NUM):
                exit(0)


if __name__ == '__main__':
    t1=threading.Thread(target=send_random_traffic)
    t1.start()
    sniff(iface = INTF,
          prn = lambda x: handle_pkt(x))

