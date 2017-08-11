import time
import os

CLI_PATH='/home/wsb/bmv2/targets/simple_switch/sswitch_CLI LBswitch.json'
CMD_PATH='weight_reset_command'

for i in range(15):
  os.system("%s < %s"%(CLI_PATH,CMD_PATH))
  time1=time.time()
  os.system("python3 psend_static.py")
  with open("time_pstatic",'a') as f:
    f.write("%f\n"%(time.time()-time1,))

