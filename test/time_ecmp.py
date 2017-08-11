import time
import os

for i in range(50):
  time1=time.time()
  os.system("python3 csend.py")
  with open("time_ecmp_f",'a') as f:
    f.write("%f\n"%(time.time()-time1,))
