import os, threading
import weight

DIP_NUM=4
VER=0
CLI_PATH='/home/wsb/bmv2/targets/simple_switch/sswitch_CLI LBswitch.json'

ts=[threading.Thread(target=os.system, args=("docker stats h%s > temp_cpu%s"%(i+1,i+1),)) for i in range(DIP_NUM)]
for t in ts:
    t.setDaemon(True)
    t.start()

VER+=1
args=weight.get_args(False)
i=0
with open('temp_commands.txt','w') as f:
    for arg in args:
        f.write('table_add route_table select_dip %d %d => %d\n'%(i,VER,arg))
        i+=1
    f.write('register_write version_register 0 %d\n'%(VER,))
    f.write('counter_reset request_counter\n')
os.system('%s < %s'%(CLI_PATH, 'temp_commands.txt'))


while(1):
    if(input()=="update"):
        VER+=1
        args=weight.get_args(True)
        i=0
        with open('temp_commands.txt','w') as f:
            for arg in args:
                f.write('table_add route_table select_dip %d %d => %d\n'%(i,VER,arg))
                i+=1
            f.write('register_write version_register 0 %d\n'%(VER,))
            f.write('counter_reset request_counter\n')
        os.system('%s < %s'%(CLI_PATH, 'temp_commands.txt'))
        for i in range(DIP_NUM):
            os.system('rm temp_cpu%s'%(i+1,))
        exit(0)

