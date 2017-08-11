import matplotlib.pyplot as plt
import numpy

with open("time_pecmp",'r') as f:
  time_ecmp=numpy.array(list(map(lambda x: float(x),f.read().split("\n")[:-1])))
with open("time_pweight",'r') as f:
  time_weig=numpy.array(list(map(lambda x: float(x),f.read().split("\n")[:-1])))
with open("time_pstatic",'r') as f:
  time_stat=numpy.array(list(map(lambda x: float(x),f.read().split("\n")[:-1])))


time_y1=numpy.arange(0,1,1/len(time_ecmp))
time_y2=numpy.arange(0,1,1/len(time_weig))
time_y3=numpy.arange(0,1,1/len(time_stat))

time_ecmp=numpy.sort(time_ecmp)
time_weig=numpy.sort(time_weig)
time_stat=numpy.sort(time_stat)

plt.plot(time_ecmp,time_y1,"g-",label="ECMP",linewidth=2)
plt.plot(time_stat,time_y3,"k--",label="static weight",linewidth=2)
plt.plot(time_weig,time_y2,"r-.",label="LBAS",linewidth=2)


plt.grid(True)
plt.legend()
plt.xlabel("delay")
plt.ylabel("CDF")


plt.show()
