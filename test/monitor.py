import re, os, time


def get_pkts():
  p=re.compile("packets=[0-9]+")
  a=os.popen("/home/wsb/bmv2/targets/simple_switch/sswitch_CLI LBswitch.json < read_commands")
  m=p.findall(a.read())
  pkts=[i.split("=")[-1] for i in m]
  return " ".join(pkts)


with open('request_static','w') as f:
  while(True):
    f.write("%s\n"%(get_pkts()))
    time.sleep(0.1)
