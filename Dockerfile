FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y tcpdump net-tools python3-pip inetutils-ping wget firefox
