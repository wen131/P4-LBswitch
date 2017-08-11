# P4 LBSwitch
### env
clone and install bmv2 and p4c-bm from github.com/p4lang
### source_routing
a modified version of tutorials/SIGCOMM2015/source_routing in github.com/p4lang
```sh
./run_demo.sh
xterm h1 h3
in h3: ./receiced.py
in h1: ./send.py h1 h3
```
now,you can modify command.txt at last line to change the Switch's behavior.

modify 1 1 to 1 0 will make it works.

### heavy_hitter
a modified version of tutorials/SIGCOMM2016/heavy_hitter in github.com/p4lang

```sh
./run_demo.sh
in mininet: xterm h1 h3
in h3: ./receive.py
in h1: ./send.py h2
in another terminal: python3 controller.py
```
#### lagecy , ignore it
now,you can see the traffic will be sent to h2 or h3 randomly depends on the dport which is randomed in send.py.

this one hash the (ip_srcAddr,ip_dstAddr,protocol,src_port,dst_port) to a 16 bit result and mod 2 to choose a target host. But, if this connection have seen before it must follow it's first route. Finally, there will be NAT step to modify ip.dstAddr and mac.dstAddr.
