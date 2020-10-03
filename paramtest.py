import matplotlib
import matplotlib.pyplot as plt
import math
import numpy as np


fun=lambda x: 20*np.sin(x)
dfun=lambda x: 20*np.cos(x)
a=-2*np.pi
b=2*np.pi


"""
fun=lambda x: np.exp(x)
dfun=lambda x: np.exp(x)
a=-10
b=3
"""

densedomain=np.linspace(a,b,500)

nsamples=50
classicsamples=np.linspace(a,b,nsamples)

paramsteps=10000
paramdelta=(b-a)/(paramsteps-1)
print("Integration step:",paramdelta)
paramsamples=np.linspace(a,b,paramsteps)
L=0.0
for i in range(paramsteps-1):
	startX=paramsamples[i]
	endX=paramsamples[i+1]
	startSlope=dfun(startX)
	endSlope=dfun(endX)
	avgSlope=0.5*(startSlope+endSlope)
	L+=paramdelta*np.sqrt(1+avgSlope**2)
print("Curve length:",L)

curvesamples=np.linspace(0,L,nsamples)
print("Samples on curve length:",curvesamples)
xcurvesamples=np.array([])
l=0.0
xt=a
for curvesample in curvesamples:
	while l<curvesample:
		startX=xt
		endX=xt+paramdelta
		startSlope=dfun(startX)
		endSlope=dfun(endX)
		avgSlope=0.5*(startSlope+endSlope)
		l+=paramdelta*np.sqrt(1+avgSlope**2)
		xt+=paramdelta
	xcurvesamples=np.append(xcurvesamples,xt)
	print("Sample at s=",l,", x=",xt)
	
fig1, ax1 = plt.subplots()
ax1.set(xlabel='x', ylabel='y',
       title='Normal sampling')
ax1.grid()

fig1, ax2 = plt.subplots()
ax2.set(xlabel='x', ylabel='y',
       title='Curvilinear sampling')
ax2.grid()
		
ax1.plot(densedomain,fun(densedomain))
ax2.plot(densedomain,fun(densedomain))

ax1.plot(classicsamples,fun(classicsamples),linestyle="None",marker="*")
ax2.plot(xcurvesamples,fun(xcurvesamples),linestyle="None",marker="*")

ax1.set_aspect('equal', 'box')
ax2.set_aspect('equal', 'box')

plt.show()
