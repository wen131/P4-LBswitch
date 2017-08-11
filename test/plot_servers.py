import numpy
import matplotlib.pyplot as plt

DIPS=list(range(4,10))
ecmp=[]
stat=[]
weig=[]
for i in DIPS:
  temp=numpy.loadtxt('time_secmp%d'%(i,))
  ecmp.append(sum(temp)/len(temp))
  temp=numpy.loadtxt('time_sstatic%d'%(i,))
  stat.append(sum(temp)/len(temp))
  temp=numpy.loadtxt('time_sweight%d'%(i,))
  weig.append(sum(temp)/len(temp))

plt.figure(figsize=(5,3.09))
plt.plot(ecmp,DIPS,'g--',label='ECMP',linewidth=3)
plt.plot(stat,DIPS,'r-.',label='Static Weight',linewidth=3)
plt.plot(weig,DIPS,'k-',label='LBAS',linewidth=3)

plt.grid(True)

leg=plt.legend()
for legobj in leg.legendHandles:
  legobj.set_linewidth(2.1)
plt.ylabel("Number of Servers")
plt.xlabel("Average Response Time (ms)")
plt.tight_layout()

plt.savefig('servers.eps', format='eps' ,dpi=1000)

plt.show()
