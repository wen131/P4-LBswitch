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
import base64
import random
import sys

INTF="eth0"

def randomword(max_length):
    length = random.randint(1, max_length)
    return ''.join(random.choice([chr(i) for i in range(65,110)]) for i in range(length))

def handle_pkt(pkt,token):
    if IP in pkt and TCP in pkt:
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        proto = pkt[IP].proto
        sport = pkt[TCP].sport
        dport = pkt[TCP].dport
        data = pkt[Raw].load
        id_tup = (src_ip, dst_ip, proto, sport, dport)
        print ("Received from %s, %s" %(id_tup,data))
        if(src_ip == "10.0.7.23" ):
            for i in range(400):
                base64.b64encode(bytes(randomword(80),encoding='utf8'))
            p = Ether(src="11:22:33:44:55:66",dst="00:00:00:23:22:11")/IP(dst=src_ip,src="7.23.7.23")
            if (data==b"end"):
                data=token
            p = p/TCP(dport=sport)/Raw(load=data)
            sendp(p, iface = INTF)

def main(token):
    sniff(iface = INTF,
          prn = lambda x: handle_pkt(x,token))

if __name__ == '__main__':
    main(sys.argv[1])
