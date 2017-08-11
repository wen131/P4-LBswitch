import os
import random

os.remove('commands.txt')
f=open('commands.txt','a')

DIP_NUM=4
HASH_CONST=32
CONTROLLER=0

f.write('table_set_default hash_table hash_action\n')
f.write('table_set_default forward nat\n')
f.write('table_set_default remeber_version remeber_action\n')
f.write('table_set_default redirect _nop\n')
f.write('table_add redirect push_to_controller 1 =>\n')
f.write('table_add sercli_table inverse_nat 118949655 =>\n')
for i in xrange(DIP_NUM):
    f.write('table_add map_table map_dip %d => %d %d %d\n'%(i,i+167772162,i+2,i+2))
for i in xrange(HASH_CONST):
    f.write('table_add route_table select_dip %d %d => %d\n'%(i,0,i%4))

f.write('mirroring_add 250 %d\n'%(CONTROLLER,))

