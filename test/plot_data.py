import random
import numpy
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import matplotlib


x=numpy.loadtxt("data_raw")
y=x[:,1]
z=x[:,2]
x=x[:,0]
print(x)

fig = plt.figure(figsize=(5,3.09))
ax = fig.gca(projection='3d')
surf=ax.plot_trisurf(x,y,z,cmap='coolwarm',antialiased=False)
fig.colorbar(surf,shrink=0.5, aspect=20)
plt.xlabel("Average CPU Usage (%)")
plt.ylabel("Number of Request")
ax.set_zlabel("Response time (s)")
fig.tight_layout()
plt.show()
