import math

class Zone:
    def __init__(self,func,dfunc,lowbound,upbound):
        ### CLASS CONSTRUCTOR
        self.func=func
        self.dfunc=derivatvefunc
        self.lowbound=lowbound
        self.upbound=upbound

    def evalF(self,x):
        ### EVALUATE FUNCTION
        if x<self.lowbound or x>self.upbound:
            raise ValueError("Evaluation point is not in the defined interval")
        return self.func(x)

    def evalDF(self,x):
        ### EVALUATE FUNCTION DERIVATIVE
        if x<self.lowbound or x>self.upbound:
            raise ValueError("Evaluation point is not in the defined interval")
        return self.dfunc(x)

class Joint:
    def __init__(self,leftzone,rightzone,leftoff,rightoff):
        self.leftzone=leftzone
        self.rightzone=rightzone
        self.leftoff=leftoff
        self.rightoff=rightoff


class ArcInterpolator:
    def __init__(self):
        self.zones=[]
        sefl.processedZones=[]
        self.joints=[]
        self.arcs=[]

    def addZone(self,func,dfunc,lowbound,upbound,filletoff=0.5)
        prevZone=None
        newZone=Zone(func,dfunc,lowbound,upbound)
        if len(self.zones):
            prevZone=self.zones[-1]
            if not math.isclose(prevZone.upbound,newZone.lowbound):
                raise ValueError("There must be no gaps in the domain")
            if not math.isclose(prevZone.evalF(prevZone.upbound),newZone.evalF(newZone.lowbound)):
                raise ValueError("There must be no gaps in the co-domain")

            if not math.isclose(prevzone.evalDF(prevZone.upbound),newZone.evalDF(newZone.lowbound)):
                newJoint=Joint(prevZone,newZone,filletoff,filletoff)
                self.joints.append(newJoint)
            else:
                self.joints.append(None)
        self.zones.append(newZone)

    def compute(self):
            self.processJoints()
            for i in range(len(self.processedZones)):
                zone=self.processedZones[i]
                arcsGenerator=ArcsGenerator(processedZone)
                arcs=arcsGenerator.computeArcs()
                self.arcs+=arcs
                if i<len(self.joints):
                    nextZone=self.processedZones[i+1]
                    leftpoint=np.array([zone.upbound,zone.evalF(zone.upbound)])
                    leftslope=zone.evalDF(zone.upbound)
                    rightpoint=np.array([nextZone.lowbound,nextZone.evalF(nextZone.lowbound)])
                    rightslope=nextZone.evalDF(nextZone.lowbound)
                    self.arcs+=BiArc(leftpoint,rightpoint,leftslope,rightslope)
            return self.arcs


    def processJoints(self):
        for i in range(len(self.zones)):
            linearZone=self.zones[i]
            curvilinearZoneAxis=CurvilinearAxis(linearZone)

            # EXCLUDE JOINTS FROM DOMAIN
            if i==0:
                lowbound=linearZone.lowbound
            else:
                joint=self.joints[i-1]
                lowbound=curvilinearZoneAxis.S2X(joint.rightoff)

            if i==len(self.joints):
                upbound=linearZone.upbound
            else:
                joint=self.joints[i]
                upbound=curvilinearZoneAxis.S2X(curvilinearZoneAxis.length-joint.leftoff)
            processedZone=Zone(linearZone.func,linearZone.dfunc,lowbound,upbound)
            self.processedZones.append(processedZone)

    def calcArcs(self):
        pass
