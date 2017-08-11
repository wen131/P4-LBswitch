import matplotlib.pyplot as plt
import numpy

import matplotlib

font = {'size':15}
matplotlib.rc('font',**font)



ecmp=numpy.loadtxt('cpu_usage_ecmp')[:,1]*100
stat=numpy.loadtxt('cpu_usage_static')[:,1]*100
weig=numpy.loadtxt('cpu_usage_weight')[:,1]*100



plt.figure(figsize=(5,3.09))

bar_width=0.25
p_ecmp=plt.bar([bar_width*(i+1) for i in range(4)],ecmp,bar_width,ec='k',ls='-',lw=2, hatch='/')
p_stat=plt.bar([bar_width*(i+7) for i in range(4)],stat,bar_width,ec='k',ls='-',lw=2, hatch='.')
p_weig=plt.bar([bar_width*(i+13) for i in range(4)],weig,bar_width,ec='k',ls='-',lw=2, hatch='o')

#leg=plt.legend()
#for legobj in leg.legendHandles:
#  legobj.set_linewidth(2.1)
plt.xticks([bar_width*i for i in [2.5,8.5,14.5]],["ECMP","Static Weight","LBAS"])
plt.ylabel("Average CPU Usage (%)")
plt.tight_layout()

plt.savefig('cpu_usage.eps',format='eps', dpi=1000)
plt.show()
