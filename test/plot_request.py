import matplotlib.pyplot as plt
import numpy

import matplotlib

font = {'size':15}
matplotlib.rc('font',**font)


ecmp=numpy.loadtxt('request_ecmp4')
stat=numpy.loadtxt('request_static4')
weig=numpy.loadtxt('request_weight4')

ecmp=numpy.array([[sum(ecmp[i,:3])/3,ecmp[i,3]] for i in range(len(ecmp))])
stat=numpy.array([[sum(stat[i,:3])/3,stat[i,3]] for i in range(len(stat))])
weig=numpy.array([[sum(weig[i,:3])/3,weig[i,3]] for i in range(len(weig))])

time1=numpy.arange(len(ecmp))*0.1
time2=numpy.arange(len(stat))*0.1
time3=numpy.arange(len(weig))*0.1

plt.figure(figsize=(5,3.09))
p_ecmp=plt.plot(time1,ecmp[:,0],"g-.",linewidth=3)
p_stat=plt.plot(time2,stat[:,0],"r-.",linewidth=3)
p_weig=plt.plot(time3,weig[:,0],"k-.",linewidth=3)
p_ecmp=plt.plot(time1,ecmp[:,1],"g-",label="ECMP",linewidth=3)
p_stat=plt.plot(time2,stat[:,1],"r-",label="Static Weight",linewidth=3)
p_weig=plt.plot(time3,weig[:,1],"k-",label="LBAS",linewidth=3)
plt.plot([3.65]*2,[-10,100],'k--',linewidth=2)

plt.axis([-0.1,6,-1,80])
plt.grid(True)
leg=plt.legend(prop={'size':14})
for legobj in leg.legendHandles:
  legobj.set_linewidth(10)
plt.xlabel("Time (s)")
plt.ylabel("Number of Requests")
plt.text(0,25,"Old Servers",rotation=26)
plt.text(1.4,3,"New Server")
plt.tight_layout()
plt.savefig('request.eps', format='eps' ,dpi=1000)

plt.show()
