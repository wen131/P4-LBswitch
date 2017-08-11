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
THR=1
PKTS_PERTHR=200
PKTS_NUM=THR*PKTS_PERTHR
INTF="veth2"

def send_random_traffic():
    random_ports = random.sample(range(1024,65535), PKTS_PERTHR)
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
    ts=[]
    for i in range(THR):
        ts.append(threading.Thread(target=send_random_traffic))
    for t in ts:
        t.start()
    sniff(iface = INTF,
          prn = lambda x: handle_pkt(x))

