import matplotlib.pyplot as plt
import numpy

import matplotlib

font = {'size':15}
matplotlib.rc('font',**font)


with open("time_cpu_pecmp",'r') as f:
  time_ecmp=numpy.array(list(map(lambda x: float(x),f.read().split("\n")[:-1])))
with open("time_cpu_pweight_50",'r') as f:
  time_weig=numpy.array(list(map(lambda x: float(x),f.read().split("\n")[:-1])))
with open("time_cpu_pstatic",'r') as f:
  time_stat=numpy.array(list(map(lambda x: float(x),f.read().split("\n")[:-1])))


time_y_ecmp=numpy.array([(i+1)*100/len(time_ecmp) for i in range(len(time_ecmp))])
time_y_weig=numpy.array([(i+1)*100/len(time_weig) for i in range(len(time_weig))])
time_y_stat=numpy.array([(i+1)*100/len(time_stat) for i in range(len(time_stat))])

time_ecmp=numpy.sort(time_ecmp)
time_weig=numpy.sort(time_weig)
time_stat=numpy.sort(time_stat)

print(time_ecmp)


plt.figure(figsize=(5,3.09))
p_ecmp=plt.plot(time_ecmp,time_y_ecmp,"g--",label="ECMP",linewidth=3)
p_stat=plt.plot(time_stat,time_y_stat,"r-.",label="Static Weight",linewidth=3)
p_weig=plt.plot(time_weig,time_y_weig,"k-",label="LBAS",linewidth=3)

plt.grid(True)
leg=plt.legend(prop={'size':14})

for legobj in leg.legendHandles:
  legobj.set_linewidth(2.1)
plt.xlabel("Average Response Time (ms)")
plt.ylabel("CDF (%)")
plt.tight_layout()
plt.savefig('light_pool.eps', format='eps' ,dpi=1000)

plt.show()
