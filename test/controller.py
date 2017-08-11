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
import os
import threading
import weight

VER=0
CLI_PATH='/home/wsb/bmv2/targets/simple_switch/sswitch_CLI LBswitch.json'

def handle_pkt(pkt):
    if IP in pkt and TCP in pkt:
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        proto = pkt[IP].proto
        sport = pkt[TCP].sport
        dport = pkt[TCP].dport
        id_tup = (src_ip, dst_ip, proto, sport, dport)
        hexdump(pkt)
        res_dst=bytes(pkt)[:6]
        res_src=bytes(pkt)[6:12]
        if int.from_bytes(res_src,byteorder='big')==723:
            hash_res=int.from_bytes(res_dst,byteorder='big')
            print(hex(hash_res))
            CMD="'table_add version_table select_version %d => %d'"%(hash_res,VER)
            do_cmd(CMD)

def do_cmd(CMD):
    os.system('echo %s | %s'%(CMD,CLI_PATH)) 

def data_plane():
    sniff(iface = "veth1",
          prn = lambda x: handle_pkt(x))

if __name__ == '__main__':
    t1=threading.Thread(target=data_plane)
    t1.start()
    while(1):
        if(input()=="update"):
            VER+=1
            args=weight.get_args()
            f=open('temp_commands.txt','w')
            i=0
            for arg in args:
                f.write('table_add route_table select_dip %d %d => %d\n'%(i,VER,arg))
                i+=1
            f.write('register_write version_register 0 %d\n'%(VER,))
            f.close()
            os.system('%s < %s'%(CLI_PATH, 'temp_commands.txt'))
            
