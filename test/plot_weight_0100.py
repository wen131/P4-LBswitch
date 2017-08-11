import matplotlib.pyplot as plt
import numpy
import matplotlib

font = {'size':15}
matplotlib.rc('font',**font)


with open("time_static",'r') as f:
  time000=numpy.array(list(map(lambda x: float(x)*5,f.read().split("\n")[:-1])))
with open("time_weight_100",'r') as f:
  time100=numpy.array(list(map(lambda x: float(x)*5,f.read().split("\n")[:-1])))


time_y000=numpy.array([(i+1)*100/len(time000) for i in range(len(time000))])
time_y100=numpy.array([(i+1)*100/len(time100) for i in range(len(time100))])

time000=numpy.sort(time000)
time100=numpy.sort(time100)



plt.figure(figsize=(5,3.09))
p000=plt.plot(time000,time_y000,"r--",label="Static Weight",linewidth=3)
p100=plt.plot(time100,time_y100,"k-",label="Full Dynamic",linewidth=3)

plt.grid(True)
#leg=plt.legend([p_ecmp, p_stat],['ECMP', 'Static Weight'])
#for legobj in leg.legendHandles:
#  legobj.set_linewidth(2.0)
leg=plt.legend(prop={'size':14})
for legobj in leg.legendHandles:
  legobj.set_linewidth(2.3)

plt.axis([80,190,-2,102])
plt.xlabel("Average Response Time (ms)")
plt.ylabel("CDF (%)")
plt.tight_layout()
plt.savefig('weight_0100.eps', format='eps' ,dpi=1000)

plt.show()
