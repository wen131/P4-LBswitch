import re

quota_arr=[40,60,40,60,40,60,40,60,40]
res=[]

for k in range(4):
    with open("cpu_record_static%s"%(k+1,),"r") as f:
        data=f.read()
    p=re.compile(r"[0-9]+.[0-9]+%")
    m=p.findall(data)
    res.append([float(m[2*i][:-2])/quota_arr[k] for i in range(len(m)//2)])
    quota=quota_arr[k-1]

assert((len(res[0])==len(res[1]))and(len(res[1])==len(res[2]))and(len(res[2])==len(res[3])))
print(res)
with open("cpu_record_static",'w') as f:
    for i in range(len(res[0])):
        f.write("%f %f %f %f\n"%(res[0][i],res[1][i],res[2][i],res[3][i]))
