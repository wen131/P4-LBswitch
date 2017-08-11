with open('time_sweight4','r') as f:
  x=list(map(lambda x: float(x),f.read().split("\n")[:-1]))
print(x)
x=map(lambda x:x-25,x)
with open('time_sweight4_raw','w') as f:
  for i in x:
    f.write('%f\n'%(i))
