import matplotlib.pyplot as plt
import numpy

import matplotlib

font = {'size':15}
matplotlib.rc('font',**font)


with open("time_ecmp",'r') as f:
  time_ecmp=numpy.array(list(map(lambda x: float(x)*5,f.read().split("\n")[:-1])))
with open("time_static",'r') as f:
  time_stat=numpy.array(list(map(lambda x: float(x)*5,f.read().split("\n")[:-1])))


time_y_ecmp=numpy.array([(i+1)*100/len(time_ecmp) for i in range(len(time_ecmp))])
time_y_stat=numpy.array([(i+1)*100/len(time_stat) for i in range(len(time_stat))])

time_ecmp=numpy.sort(time_ecmp)
time_stat=numpy.sort(time_stat)

print(time_ecmp)


plt.figure(figsize=(5,3.09))
p_ecmp=plt.plot(time_ecmp,time_y_ecmp,"r--",label="ECMP",linewidth=3)
p_stat=plt.plot(time_stat,time_y_stat,"k-",label="Static Weight",linewidth=3)

plt.grid(True)
#leg=plt.legend([p_ecmp, p_stat],['ECMP', 'Static Weight'])
#for legobj in leg.legendHandles:
#  legobj.set_linewidth(2.0)
leg=plt.legend(prop={'size':14})
for legobj in leg.legendHandles:
  legobj.set_linewidth(2.3)
plt.xlabel("Average Response Time (ms)")
plt.ylabel("CDF (%)")
plt.tight_layout()
plt.savefig('motivation.eps', format='eps' ,dpi=1000)

plt.show()
