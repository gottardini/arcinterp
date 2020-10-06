import matplotlib
import matplotlib.pyplot as plt

import numpy as np
import geometries as gm



#Functions declaration
fun=lambda x: np.sin(x)
dfun=lambda x: np.cos(x)
a=0
b=2*np.pi

#Plot setup
fig, ax = plt.subplots()
ax.set(xlabel='x', ylabel='y',
       title='BiArc Test')
ax.grid()

#Fixed samples arcs
fixed_samples=np.linspace(a,b,15)
fixed_arcs=[]
for i in range(len(fixed_samples)-1):
	SP=np.array([fixed_samples[i],fun(fixed_samples[i])])
	EP=np.array([fixed_samples[i+1],fun(fixed_samples[i+1])])
	SS=dfun(fixed_samples[i])
	ES=dfun(fixed_samples[i+1])
	fixed_arcs.append(BiArc(SP,EP,SS,ES,fun))

#Plot original function
xspace=np.linspace(a,b,500)
ax.plot(xspace, fun(xspace), color="black")
ax.plot(fixed_samples,fun(fixed_samples),linestyle="None",marker="*")

#plot fixed samples biarc interpolation
for biarc in fixed_arcs:
	biarc.computeArcs()
	biarc.plot(ax)

fig.savefig("test.png")
plt.show()
