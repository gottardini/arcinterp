import matplotlib
import matplotlib.pyplot as plt
import math
import numpy as np

class Line:
	def __init__(self,startPoint,endPoint):
		self.startPoint=startPoint
		self.endPoint=endPoint
		
	def plot(self,ax):
		ax.plot(np.array([self.startPoint[0],self.endPoint[0]]),np.array([self.startPoint[1],self.endPoint[1]]))

class Arc:
	def __init__(self,centerPoint=None,startPoint=None,endPoint=None,radius=None,startAngle=None,endAngle=None):
		#CENTER POINT MUST BE PROVIDED
		if centerPoint is None:
			raise ValueError("Arc center point must be provided")
		self.centerPoint=centerPoint
		
		#AT LEAST ONE AND ONLY ONE BETWEEN ARC POINT OR ANGLE CAN BE PROVIDED 
		if (startPoint is not None and startAngle is not None)  or \
		   (endPoint   is not None and endAngle   is not None)    or \
		   (startPoint is     None and startAngle is     None)  or \
		   (endPoint   is     None and endAngle   is     None):        
			raise ValueError("Wrong input arguments. You must provide one and only one between point and angle")
			
		#RADIUS MUST BE PROVIDED IF NO POINT IS GIVEN (UNDERCONSTRAINT)
		if startPoint is None and endPoint is None and radius is None:
			raise ValueError("You must provide radius if no points are given")
			
		#RADIUS MUST NOT BE PROVIDED IF AT LEAST ONE POINT IS GIVEN (OVERCONSTRAINT)
		if (startPoint is not None or endPoint is not None) and radius is not None:
			raise ValueError("You mustn't provide radius if at least one point is given")
			
		### AT THIS POINT THE INPUT PARAMETERS CAN BE
		###
		### 1.    startPoint= None    endPoint= None    radius!=None    startAngle!=None    endAngle!=None
		### 2.    startPoint= None    endPoint!=None    radius= None    startAngle!=None    endAngle= None
		### 3.    startPoint!=None    endPoint= None    radius= None    startAngle= None    endAngle!=None    
		### 4.    startPoint!=None    endPoint!=None    radius= None    startAngle= None    endAngle= None
		
		#LETS CALCULATE RADIUS IF NEEDED AND CHECK IF ITS OVERCONSTRAINED
		if radius is not None: #already has a value, noprob then. Calculate points. CASE NO. 1
			self.startPoint=self.calcPoint(startAngle)
			self.endPoint=self.calcPoint(endAngle)
		else:
			if startPoint is not None:
				self.radius=self.calcRadius(startPoint)
			if endPoint is not None:
				if self.radius is not None:
					rad2=self.calcRadius(endPoint)
					if not math.isclose(self.radius,rad2):
						raise ValueError("The 2 points provided don't lay on the same arc: radiuses are %s and %s"%(self.radius,rad2))
				else:
					self.radius=self.calcRadius(endPoint)
			# CASES 2,3,4
			if startPoint is None: #2
				self.startPoint=self.calcPoint(startAngle)
				self.startAngle=startAngle
			else: #3,4
				self.startAngle=self.calcAngle(startPoint)
				self.startPoint=startPoint
				
			if endPoint is None: #3
				self.endPoint=self.calcPoint(endAngle)
				self.endAngle=endAngle
			else: #2,4
				self.endAngle=self.calcAngle(endPoint)
				self.endPoint=endPoint
					
	def calcPoint(self, angle):
		return self.centerPoint+np.array([self.radius*np.cos(angle), self.radius*np.sin(angle)])
		
	def calcAngle(self, point):
		return np.arctan2((point-self.centerPoint)[1],(point-self.centerPoint)[0])
		
	def calcRadius(self, point):
		return np.linalg.norm(point-self.centerPoint)
		
	def sample(self, x):
		ang=np.arccos((x-self.centerPoint[0])/self.radius)
		ang=np.where(self.startAngle>ang or self.endAngle<ang, -ang, ang)
		return self.centerPoint[1]+self.radius*np.sin(ang) 
		
	def plot(self,ax):
		angspace=np.linspace(self.startAngle,self.endAngle,10)
		x=self.centerPoint[0]+self.radius*np.cos(angspace)
		y=self.centerPoint[1]+self.radius*np.sin(angspace)
		ax.plot(x,y,color="cyan")
			
		

class BiArc:
	def __init__(self,startPoint,endPoint,startSlope,endSlope,fun):
		self.startPoint=startPoint
		self.endPoint=endPoint
		self.startSlope=startSlope
		self.endSlope=endSlope
		self.fun=fun
		self.arc1=None
		self.arc2=None

	def computeArcs(self):
		segment=self.endPoint-self.startPoint
		segmentLength=np.linalg.norm(segment)
		psi=np.arctan2(segment[1],segment[0])
		arg_tStart=np.arctan(self.startSlope)
		arg_tEnd=np.arctan(self.endSlope)
		tStart=np.array([np.cos(arg_tStart),np.sin(arg_tStart)])
		nStart=np.array([-np.sin(arg_tStart),np.cos(arg_tStart)])
		tEnd=np.array([np.cos(arg_tEnd),np.sin(arg_tEnd)])
		nEnd=np.array([-np.sin(arg_tEnd),np.cos(arg_tEnd)])
		alpha=psi-arg_tStart
		beta=arg_tEnd-psi
		if alpha*beta>0:
			theta=alpha
		else:
			theta=(3*alpha-beta)/2
		tMiddle=np.array([np.cos(theta+arg_tStart),np.sin(theta+arg_tStart)])
		nMiddle=np.array([-np.sin(theta+arg_tStart),np.cos(theta+arg_tStart)])
		
		print(alpha,beta)
		if (math.isclose(theta,0) or math.isclose(alpha+beta,0)) and (math.isclose(alpha+beta-theta,0) or math.isclose(alpha+beta,0)):
			self.arc1=Line(self.startPoint,self.endPoint)
		elif math.isclose(theta,0) or math.isclose(alpha+beta,0) or math.isclose(alpha+beta-theta,0):
			raise ValueError("Cannot build biarc with the given specs")
		else:
			r1=segmentLength/(2*np.sin((alpha+beta)/2))*np.sin((beta-alpha+theta)/2)/np.sin(theta/2)
			r2=segmentLength/(2*np.sin((alpha+beta)/2))*np.sin((2*alpha-theta)/2)/np.sin((alpha+beta-theta)/2)
			middlePoint=self.startPoint+r1*(nStart-nMiddle)
			O1=self.startPoint+r1*nStart
			O2=middlePoint+r2*nMiddle
			self.arc1=Arc(centerPoint=O1, startPoint=self.startPoint, endPoint=middlePoint)
			self.arc2=Arc(centerPoint=O2, startPoint=middlePoint, endPoint=self.endPoint)
			print(r1,r2)
		
	def estimateError(self):
		segment=self.endPoint-self.startPoint
		segmentLength=np.linalg.norm(segment)
		psi=np.arctan2(segment[1],segment[0])
		arg_tStart=np.arctan(self.startSlope)
		arg_tEnd=np.arctan(self.endSlope)
		alpha=psi-arg_tStart
		beta=arg_tEnd-psi
		db=np.linalg.norm(self.endPoint-self.startPoint)/2*np.abs(np.tan(alpha/2)-np.tan(beta/2))
		dm=db/13.5
		testingPoints=np.linspace(startPoint,endPoint,7)
		
		
		
	def plot(self,ax):
		if self.arc1:
			self.arc1.plot(ax)
		if self.arc2:
			self.arc2.plot(ax)
		
		"""	
		rad11=self.startPoint-self.O1
		arg11=np.arctan2(rad11[1],rad11[0])
		rad12=self.middlePoint-self.O1
		arg12=np.arctan2(rad12[1],rad12[0])
		rad21=self.middlePoint-self.O2
		arg21=np.arctan2(rad21[1],rad21[0])
		rad22=self.endPoint-self.O2
		arg22=np.arctan2(rad22[1],rad22[0])
		arg1space=np.linspace(arg11,arg12,10)
		arg2space=np.linspace(arg21,arg22,10)
		x1=self.O1[0]+np.abs(self.r1)*np.cos(arg1space)
		x2=self.O2[0]+np.abs(self.r2)*np.cos(arg2space)
		y1=self.O1[1]+np.abs(self.r1)*np.sin(arg1space)
		y2=self.O2[1]+np.abs(self.r2)*np.sin(arg2space)
		ax.plot(x1,y1,color="yellow")
		ax.plot(x2,y2,color="cyan")
		"""

###START

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


