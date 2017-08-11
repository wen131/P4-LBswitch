DIP_NUM=4
HASH_CONST=32
BASE=[0,0,0,0,1,1,1,1,1,1,2,2,2,2,0,0,0,0,1,1,1,1,1,1,2,2,2,2,0,1,1,2]

with open("weight_reset_command",'w') as f:
  f.write('table_clear route_table\n')
  f.write('register_write version_register 0 0\n')
  for i in range(HASH_CONST):
    f.write('table_add route_table select_dip %d %d => %d\n'%(i,0,BASE[i]))

