with open("data60","r") as f:
  data=f.read()
  data=data.split("\n")
x=[[sum(list(map(lambda x:float(x),data[i].split(" ")[:3])))*100/3, data[i].split(" ")[3]] for i in range(len(data)-1)]
y=[float(data[i].split(" ")[-1]) for i in range(len(data)-1)]
with open("data_raw","w") as f:
  for i in range(len(x)-1):
    f.write("%f %s %s\n"%(x[i][0],x[i][1],y[i]))
