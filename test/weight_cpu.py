import random, os, re
from sklearn.externals import joblib

DIP_NUM=4
BASE_HASH=16
DYNAMIC_HASH=16

quota_arr=[40,60,40,60]
clf0=joblib.load("ridge40_cpu")#40
clf1=joblib.load("ridge60_cpu")#60
clfs={40:clf0,60:clf1}

BASE=[0,0,1,1,1,2,2,3,3,3,0,1,1,2,3,3]

def cpu_ans(k):
    with open("temp_cpu%s"%(k,),"r") as f:
        data=f.read()
    p=re.compile(r"[0-9]+.[0-9]+%")
    m=p.findall(data)
    res1=[float(m[2*i][:-2]) for i in range(len(m)//2)]
    quota=quota_arr[k-1]
    return sum(res1)/len(res1)/quota

def calculate_weight(levels):
  s=float(sum(levels))
  return map(lambda level: level/s ,levels)

def calculate_args(weights):
  temp=list(map(lambda x: int(x*DYNAMIC_HASH+0.5),weights))
  print(temp)
  if(sum(temp)-DYNAMIC_HASH>0):
    for i in range(sum(temp)-DYNAMIC_HASH):
      temp[temp.index(max(temp))]-=1
  if(sum(temp)-DYNAMIC_HASH<0):
    for i in range(DYNAMIC_HASH-sum(temp)):
      temp[temp.index(min(temp))]+=1
  print(temp)
  assert(sum(temp)==DYNAMIC_HASH)
  res=[]
  for i in range(len(temp)):
    for j in range(temp[i]):
      res.append(i)
  assert(len(res)==DYNAMIC_HASH)
  res.extend(BASE)
  assert(len(res)==DYNAMIC_HASH+BASE_HASH)
  return res

def get_pkts():
  p=re.compile("packets=[0-9]+")
  a=os.popen("/home/wsb/bmv2/targets/simple_switch/sswitch_CLI LBswitch.json < pkt_commands")
  m=p.findall(a.read())
  return m

def get_indata():
  pkts=get_pkts()
  indata=[cpu_ans(i+1) for i in range(DIP_NUM)]
  return indata

def norm(indata):
  indata=list(map(lambda x: x<0.4 and 0.4 or x,indata))
  indata=list(map(lambda x: x>0.8 and 0.8 or x,indata))
  return indata

def get_args(first):
  if first :
    indata=get_indata()
    print(indata)
    indata=norm(indata)
    indata=list(map(lambda x: [float(x),19],indata))
    print(indata)
    levels=[10/clfs[quota_arr[i]].predict(indata[i]).take(0) for i in range(DIP_NUM-1)]+[30]
    print(levels)
  else :
    levels=quota_arr
  weights=calculate_weight(levels)
  return calculate_args(weights)

if __name__ == "__main__":
  indata=range(1,50)
  print([clfs[60].predict(indata[i]).take(0) for i in range(len(indata))])
