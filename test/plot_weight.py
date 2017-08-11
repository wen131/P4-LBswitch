import matplotlib.pyplot as plt
import numpy

import matplotlib

font = {'size':15}
matplotlib.rc('font',**font)


with open("time_weight",'r') as f:
  time25=numpy.array(list(map(lambda x: float(x)*5,f.read().split("\n")[:-1])))
with open("time_weight_37",'r') as f:
  time37=numpy.array(list(map(lambda x: float(x)*5,f.read().split("\n")[:-1])))
with open("time_weight_50",'r') as f:
  time50=numpy.array(list(map(lambda x: float(x)*5,f.read().split("\n")[:-1])))
with open("time_weight_62",'r') as f:
  time62=numpy.array(list(map(lambda x: float(x)*5,f.read().split("\n")[:-1])))
with open("time_weight_75",'r') as f:
  time75=numpy.array(list(map(lambda x: float(x)*5,f.read().split("\n")[:-1])))


time_y25=numpy.array([(i+1)*100/len(time25) for i in range(len(time25))])
time_y37=numpy.array([(i+1)*100/len(time37) for i in range(len(time37))])
time_y50=numpy.array([(i+1)*100/len(time50) for i in range(len(time50))])
time_y62=numpy.array([(i+1)*100/len(time62) for i in range(len(time62))])
time_y75=numpy.array([(i+1)*100/len(time75) for i in range(len(time75))])

time25=numpy.sort(time25)
time37=numpy.sort(time37)
time50=numpy.sort(time50)
time62=numpy.sort(time62)
time75=numpy.sort(time75)



plt.figure(figsize=(5,3.09))
p25=plt.plot(time25,time_y25,"r--",label="25%",linewidth=3)
p37=plt.plot(time37,time_y37,"y-.",label="37.5%",linewidth=3)
p50=plt.plot(time50,time_y50,"k-",label="50%",linewidth=3)
p62=plt.plot(time62,time_y62,"k--",label="62.5%",linewidth=3)
p75=plt.plot(time75,time_y75,"g-.",label="75%",linewidth=3)

plt.grid(True)
#leg=plt.legend([p_ecmp, p_stat],['ECMP', 'Static Weight'])
#for legobj in leg.legendHandles:
#  legobj.set_linewidth(2.0)
leg=plt.legend(prop={'size':14})
for legobj in leg.legendHandles:
  legobj.set_linewidth(2.1)
plt.xlabel("Average Response Time (ms)")
plt.ylabel("CDF (%)")
plt.tight_layout()
plt.savefig('weight.eps', format='eps' ,dpi=1000)

plt.show()
