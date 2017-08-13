FROM ubuntu:14.04

RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip3 install scapy-python3
