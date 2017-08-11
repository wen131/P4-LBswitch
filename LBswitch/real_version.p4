/* Copyright 2013-present Barefoot Networks, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "includes/headers.p4"
#include "includes/parser.p4"

#define HASH_CONST 32
#define HASH_CONST_BIT 5
#define MAX_DIP_BIT 3
#define MAX_DIP_NUM 8
#define VER_BIT 6
#define MAX_ROUTE_NUM 2048

#define CONTROLLER_SESSION_ID 250
#define SPECIAL_SRC_MAC 723

#define VIP 118949655
#define CLIENT_PORT 1

field_list ipv4_checksum_list {
        ipv4.version;
        ipv4.ihl;
        ipv4.diffserv;
        ipv4.totalLen;
        ipv4.identification;
        ipv4.flags;
        ipv4.fragOffset;
        ipv4.ttl;
        ipv4.protocol;
        ipv4.srcAddr;
        ipv4.dstAddr;
}

field_list_calculation ipv4_checksum {
    input {
        ipv4_checksum_list;
    }
    algorithm : csum16;
    output_width : 16;
}

calculated_field ipv4.hdrChecksum  {
    verify ipv4_checksum;
    update ipv4_checksum;
}

action _drop() {
    drop();
}

header_type custom_metadata_t {
    fields {
        num: MAX_DIP_BIT;
        mod: HASH_CONST_BIT;
        hash: 16;
        mac: 48;
        ip: 32;
        port: MAX_DIP_BIT;
        version: VER_BIT;
    }
}

metadata custom_metadata_t m_metadata;

action nat() {
    modify_field(ipv4.dstAddr, m_metadata.ip);
    modify_field(standard_metadata.egress_spec, m_metadata.port);
    add_to_field(ipv4.ttl, -1);
    modify_field(ethernet.dstAddr, m_metadata.mac);
}

// TODO: Define the field list to compute the hash on
// Use the 5 tuple of 
// (src ip, dst ip, src port, dst port, ip protocol)

field_list hash_fields {
    ipv4.srcAddr;
    ipv4.dstAddr;
    ipv4.protocol;
    tcp.srcPort;
    tcp.dstPort;
}

field_list_calculation tcp_hash {
    input { 
        hash_fields;
    }
    algorithm : crc16;
    output_width : 16;
}

counter request_counter {
    type: packets;
    direct: map_table;
}

// TODO: Define the registers to store info
action select_dip(dip_num) {
    modify_field(m_metadata.num, dip_num);
}

action hash_action(){
    modify_field_with_hash_based_offset(m_metadata.mod, 0, tcp_hash, HASH_CONST);
    modify_field_with_hash_based_offset(m_metadata.hash, 0, tcp_hash, 65536);
}

action select_version(ver){
    modify_field(m_metadata.version, ver);
}

action map_dip(ip, mac, port){
    modify_field(m_metadata.ip, ip);
    modify_field(m_metadata.mac, mac);
    modify_field(m_metadata.port, port);
}

field_list remember_fields {
    standard_metadata;
    m_metadata.hash;
}

register version_register {
    width: VER_BIT;
    instance_count: 1;
}

action remeber_action(){
    clone_ingress_pkt_to_egress(CONTROLLER_SESSION_ID, remember_fields);
    register_read(m_metadata.version, version_register, 0);
}

action inverse_nat(){
    modify_field(ipv4.srcAddr,VIP);
    modify_field(standard_metadata.egress_spec, CLIENT_PORT);
}

action _nop(){
}

// TODO: Define the tables to run actions
table sercli_table {
    reads {
        ipv4.srcAddr : exact;
    }
    actions {
        inverse_nat;
    }
    size : MAX_DIP_NUM;
}

table hash_table {
    actions {
        hash_action;
    }
    size: 1;
}

table version_table {
    reads {
        m_metadata.hash : exact;
    }
    actions {
        select_version;
    }
    size: 65536;
}

table remeber_version {
    actions {
        remeber_action;
    }
    size: 1;
}

table route_table {
    reads {
        m_metadata.mod : exact;
        m_metadata.version : exact;
    }
    actions {
        select_dip;
    }
    size: MAX_ROUTE_NUM;
}

table map_table {
    reads {
        m_metadata.num : exact;
    }
    actions {
        map_dip;
    }
    size: MAX_DIP_NUM;
}

table forward {
    actions {
        nat;
    }
    size: 1;
}

control ingress {
    apply(sercli_table){
        miss{
            apply(hash_table);
            apply(version_table){
                miss{
                    apply(remeber_version);
                }
            }
            apply(route_table);
            apply(map_table);
            apply(forward);
        }
    }
}


action push_to_controller() {
    modify_field(ethernet.srcAddr, SPECIAL_SRC_MAC);
    modify_field(ethernet.dstAddr, m_metadata.hash);
}

table redirect {
    reads {
        standard_metadata.instance_type : exact;
    }
    actions {
        _nop;
        push_to_controller;
    }
    size: 1;
}

control egress {
    apply(redirect);
}
