import numpy as np

class CurvilinearAxis:
    def __init__(self,zone):
        self.zone=zone
        self.mapCurve()

    def mapCurve(self,integrationSamples=1e4):
        xLength=self.zone.upbound-self.zone.lowbound
        integrationStep=xLength/(integrationSamples-1)
        integrationDomain=np.linspace(self.zone.lowbound,self.zone.upbound,integrationSamples)
        curvilinearDomain=np.empty(integrationSamples)
        S=0.0
        for i in range(paramsteps-1):
            curvilinearDomain[i]=S
        	startX=integrationDomain[i]
        	endX=integrationDomain[i+1]
        	startSlope=self.zone.evalDF(startX)
        	endSlope=self.zone.evalDF(endX)
        	avgSlope=0.5*(startSlope+endSlope)
        	S+=paramdelta*np.sqrt(1+avgSlope**2)
        self.linearDomain=integrationDomain
        self.curvilinearDomain=curvilinearDomain
        self.length=S

    def X2S(self,x):
        idx=(np.abs(self.linearDomain-x)).argmin()
        return self.curvilinearDomain[idx]

    def S2X(self,s):
        idx=(np.abs(self.curvilinearDomain-s)).argmin()
        return self.linearDomain[idx]
