import numpy as np

class ArcsGenerator:
    def __init__(self,zone,minArcs=15,maxTolAbs=0.1):
        if minArcs%2 != 0:
            raise ValueError("Number of arcs for each zone must be even (it's bi-arc built)")
        self.zone=zone
        self.nArcs=minArcs
        self.maxTolAbs=maxTolAbs
        self.curvilinearZoneAxis=CurvilinearAxis(self.zone)

    def generateSampleSpace(self):
        nSamples=(self.nArcs/2)+1
        curvilinearSamples=np.linspace(0,self.curvilinearZoneAxis.length,nSamples)
        samples=[self.curvilinearZoneAxis.S2X(s) for s in curvilinearSamples]
        return samples

    def computeArcs(self):
        error=np.inf
        while error>self.maxTolAbs:
            samples=generateSampleSpace()
            error=0.0
            arcChain=[]
            for i in range(self.nSamples-1):
                leftX=samples[i]
                rightX=samples[i+1]
                leftY=self.zone.evalF(leftX)
                rightY=self.zone.evalF(rightX)
                leftSlope=self.zone.evalDF(leftX)
                rightSlope=self.zone.evalDF(rightX)
                leftPoint=np.array([leftX,leftY])
                rightPoint=np.array([rightX,rightY])
                biarc=BiArc(leftPoint,rightPoint,leftSlope,rightSlope,self.zone.func)
                try:
                    arcChain+=biarc.compute()
                    err=biarc.estimateError()
                    error=max(error,err)
                except Exception as e:
                    print("Could not generate an arc chain:",e)
                    return False
            self.nArcs*=2
        return arcChain
