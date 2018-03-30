#!/usr/bin/env python
# -*-coding:Utf-8 -*
import pdb

import math

# a Point can be define by:
# - cartesian coordinate list or 
class Point:
    def __init__(self,*args,**kwargs):
        self.defaultCoordName=['x','y','z','t']

        self.coord=list()
        if len(args)==0 and len(kwargs)!=0:
            for k,v in kwargs.items(): 
                setattr(self,k,v)
                self.coord.append(v)
        elif len(args)!=0 and len(kwargs)==0:
            if isinstance(args[0],list):
                self.coord = args[0]
                for i in range(len(self.coord)):
                    if len(args)<=4:
                        setattr(self,self.defaultCoordName[i],self.coord[i])
                    else:
                        setattr(self,'a'+i,self.coord[i])
                    
            else:
                for i in range(len(args)):
                    if len(args)<=4:
                        setattr(self,self.defaultCoordName[i],args[i])
                    else:
                        setattr(self,'a'+i,args[i])
                    self.coord.append(args[i])


    def __repr__(self):
        coord=[str(c) for c in self.coord]
        return '<Point: ({})>'.format(",".join(coord))

    def __add__(self,P):
        if len(P.coord)!=len(self.coord):
            raise ValueError("Point to add are not same dimension")

        addedCoord=[self.coord[i]+P.coord[i] for i in range(len(self.coord))]
            
        return Point(addedCoord)

    def __sub__(self,P):
        if len(P.coord)!=len(self.coord):
            raise ValueError("Point to add are not same dimension")

        addedCoord=[self.coord[i]-P.coord[i] for i in range(len(self.coord))]
            
        return Point(addedCoord)



###############################################################################
## Vector
# Define a vector.
# creation possible with: 
# - 2 class Point
# - 1 class Point and coordinate (scalare with tuple, list of N values for angles)
# - coordinate only
class Vector:
    def __init__(self,*args,**kwargs):
        self.origin = None
        self.end    = None
        self.coord  = None
        self.norme  = None
        self.angle  = None
        self.angleUnit = None
        #pdb.set_trace()

        for k,v in kwargs.items(): 
            if k=='angle':
                v=list(v)
                self.angleUnit=v.pop(len(v)-1)
            setattr(self,k,v)

        if len(args)>0:
            if isinstance(args[0],Point):
                self.origin = args[0]
                if len(args)>1:
                    if isinstance(args[1],Point): #vecteur entre 2 points
                        self.end = args[1]

                    elif isinstance(args[1],tuple): #vecteur entre 1 points origine et des coordonnee scalaire
                        self.end = self.origin + Point(list(args[1]))

                    elif type(args[1]) in [int,long,float]: #vecteur entre 1 points origine et des coordonnee polaire
                        self.norme = args[1]
                        if self.angle==None: 
                            self.angle=list(args[2])
                            self.angleUnit=self.angle.pop(len(self.angle)-1)


            elif isinstance(args[0],tuple): #vecteur en coordonnee scalaire
                self.coord = args[0]

            elif type(args[0]) in [int,long,float]: #vecteur en coordonnee polaire
                self.norme = args[0]
                if self.angle==None: 
                    self.angle=list(args[1])
                    self.angleUnit=self.angle.pop(len(self.angle)-1)


        if self.coord == None:
            if self.end != None:
                self.coord=tuple((self.end-self.origin).coord)

            elif  self.norme != None:
                if self.angleUnit=='deg':
                    angles=[math.radians(float(a)) for a in self.angle]

                    self.coord=list()
                    for i in range(len(angles)+1):
                        c=1
                        for j in range(len(angles)):
                            if j==len(angles)-1: c*=self.norme*math.cos(angles[j])
                            else:                c*=self.norme*math.sin(angles[j])

                        self.coord.append(c)

        if self.norme==None:
            self.norme=self.getNorme()

        if self.angle==None:
            self.angle,self.angleUnit=self.getAngle()

        if self.origin != None and self.end == None:
            self.end=Point(self.coord)

    def cartesianToSpheric(self):
        '''x1 = r.cosA1
           x2 = r.sinA1cosA2
           ...
           xn = r.cosAn.Prod(i=1 to N-1)(sinAi)
        '''
        pass
    def sphericToCartesian(self):
        '''A1 = acos(x1/r)
           A2 = acos(x2/(r.sinA1))
           ...
           An = acos(xn/(r.Prod(i=1 to N-1)(sinAi)))
        '''
        pass

    def getNorme(self):
        return (sum([i**2 for i in self.coord]))**.5
    def getAngle(self):
        self.norme=self.getNorme()
        angle=list()
        for j in range(len(self.coord)-1,0,-1):
            if self.coord[j-1]==0:
                a = math.asin(self.coord[j])
            else:            
                a = math.atan(self.coord[j]/self.coord[j-1])

            if self.coord[j-1]<0:
                a = math.pi + a
            elif  self.coord[j]<0:
                a = 2*math.pi - a

            #if j == len(self.coord)-1: a=math.acos(self.coord[j]/self.norme)
            #else:                      a=math.acos(self.coord[j]/(self.norme*math.sin(angle[j-1])))

            angle.append(a)

        if self.angleUnit==None: self.angleUnit='deg'

        if self.angleUnit=='deg':
            angle=[math.degrees(a) for a in angle]
            angleUnit='deg'
        else:
            angleUnit='rad'

        if len(self.coord)==3:
            b=math.acos(math.radians(self.coord[2]/self.getNorme()))
            if self.angleUnit=='deg' or self.angleUnit==None:
                b=math.degrees(a)
                angleUnit='deg'
            else:
                angleUnit='rad'

        return angle,angleUnit

    def cosAlpha(self,V):
        return self.scalaire(V)/(self.norme*V.norme)

    def __repr__(self):
        return '<Vector: orig={}, coord={},||v||={},angle={} {}>'.format(self.origin,self.coord,self.norme,self.angle,self.angleUnit)

    def __add__(self,other):   # On definit le comportement de la classe vis-a-vis de l'addition
        newCoord=list()
        if type(other) in [float, int, long]: # Avec un nombre
            for c in self.coord:
                newCoord.append(c+other)

        elif isinstance(other, Vecteur): # Avec un vecteur
            for i in range(len(self.coord)):
                newCoord.append(other.coord[i]+self.coord[i])

        return Vector(self.origin,newCoord)

    __radd__ = __add__ # On definit l'addition a gauche pour garantir la commutativite

    # Multiplication:
    def __mul__(self, other): # On definit le comportement de la classe vis-a-vis de la multiplication
        newCoord=list()
        if type(other) in [float, int, long]: # Avec un nombre
            for c in self.coord:
                newCoord.append(c*other)

        elif isinstance(other, Vecteur): # Avec un vecteur
            for i in range(len(self.coord)):
                newCoord.append(self.coord[(i+1)%len(self.coord)]*other.coord[(i+2)%len(self.coord)]-other.coord[(i+1)%len(self.coord)]*self.coord[(i+2)%len(self.coord)])

        return Vector(self.origin,newCoord)

    __rmul__ = __mul__ # On definit le produit vectoriel a gauche

    def translat(self,P):
        if self.origin != None:
            return Vector(self.origin+(P-self.origin),self.coord)

    def invert(self):
        if self.origin != None:
            return Vector(self.end,self.origin)

    def scalaire(self, other):
        '''
        Effectue le produit scalaire entre 2 vecteurs.
        '''
        return sum([i*j for i,j in zip(self.coord,other.coord)])

    def normaliser(self):
        '''
        Normalise le vecteur.
        '''
        self.coord=list([c/self.norme for c in self.coord])


    def isHorizontal(self):
        if self.angleUnit=='deg':
            return float(self.angle%180)==float(0)
        else:
            return float(self.angle%math.pi)==float(0)
    def isVertical(self):
        if self.angleUnit=='deg':
            return float(self.angle%180)==float(90)
        else:
            return float(self.angle%math.pi)==float(math.pi/2)

    def getPosition(self,Ptest):
        pos=list()
        for i in range(len(self.coord)):
            end1=self.end.coord[(i+1)%len(self.coord)]
            end2=self.end.coord[(i+2)%len(self.coord)]
            origin1 = self.origin.coord[(i+1)%len(self.coord)]
            origin2 = self.origin.coord[(i+2)%len(self.coord)]
            ptest1 = Ptest.coord[(i+1)%len(Ptest.coord)]
            ptest2 = Ptest.coord[(i+2)%len(Ptest.coord)]

            pos.append((end1-origin1)*(ptest2-origin2)-(ptest1-origin1)*(end1-origin1))        

        return ( (self.end.coord[0] - self.origin.coord[0]) * (Ptest.coord[1] - self.origin.coord[1])
           - (Ptest.coord[0] - self.origin.coord[0]) * (self.end.coord[1] - self.origin.coord[1]) )

    def isOnLine(self,Ptest):
        return self.getPosition(Ptest) == 0
    def isLeft(self,Ptest,online=True):
        pos=self.getPosition(Ptest)
        if online: return pos >= 0
        else:      return pos >  0
    def isRight(self,Ptest,online=True):
        pos=self.getPosition(Ptest)
        if online: return pos <= 0
        else:      return pos <  0

    def isColineaire(self,V):
        return self.x*V.y==self.y*V.z and self.y*V.z==self.z*V.x
    def isOrthogonal(self,V):
        return self.scalaire(V)==0


###############################################################################
class polygon2D:
    def __init__(self,elemList):
        self.pointList=[]
        self.vectorList=[] 

        if isinstance(elemList[0],Point):
            self.pointList=elemList

            self.vectorList = self.getVectorList(elemList)

        if isinstance(elemList[0],Vector):
            self.vectorList=elemList

            self.pointList=self.getPointList(elemList)

        self.origin = self.pointList[0]

    def getVectorList(self,elemList):
        return [Vector(self.pointList[i],self.pointList[(i+1)%len(self.pointList)]) for i in range(len(elemList))]
    def getPointList(self,elemList):
        return [v.origin for v in self.vectorList]

    def orientation(self):
        n=len(self.vectorList)
        isrightNbr=0

        isrightList=[self.vectorList[i].isRight(self.pointList[(i+2)%len(self.pointList)],True) for i in range(n)]

        for i in range(n):
            if isrightList[i]: isrightNbr+=1

        if isrightNbr==n:   return 1  #clockwise
        elif isrightNbr==0: return -1 #counterclockwise
        else:               return 0  #degenerate

    def orientate(self,orientation):
        if self.orientation()==orientation:
            pass

        n=len(self.vectorList)
        isrightNbr=0
        isrightList=[self.vectorList[i].isRight(self.pointList[(i+2)%len(self.pointList)],True) for i in range(n)]

        for i in range(n):
            if orientation==1 and not isrightList[i]:
                self.vectorList[i].invert()
            elif orientation==0 and isrightList[i]:
                self.vectorList[i].invert()

    def area(self):
        n=len(self.pointList)

        area = 0;
        if n < 3: return 0  # a degenerate polygon
 
        j=2
        k=0
        for i in range(1,n+1):
            area += self.pointList[i].x * (self.pointList[j].y - self.pointList[k].y)
            j+=1
            k+=1

        area += self.pointList[n].x * (self.pointList[1].y - self.pointList[n-1].y)  # wrap-around term
        return float(area) / 2.0;

    def turn(self,newOrigin):
        if newOrigin not in self.pointList: return None

        for i in range(len(self.pointList)):
            if self.pointList[i]==newOrigin:
                newPointList=[self.pointList[j] for j in range(i,(i+len(self.pointList))%len(self.pointList))]
        self.pointList = newPointList

    def translat(self,newOrigin):
        for i in range(len(self.pointList)):
            if self.pointList[i]==newOrigin:
                newPointList=[self.pointList[j] for j in range(i,(i+len(self.pointList))%len(self.pointList))]
        self.pointList = newPointList
        self.vectorList = self.getVectorList(newPointList)

    def rotate(self,angles,angleUnit='rad',V=None):
        '''rotate around axes x,y,z,...
           angles is list of angle to rotate, axis by axis, [x,y,z,...]
           rotation matrix is around axe u = Ru=[[cosA,-sinA],[sinA,cosA]]
           newVector=vector[[a],[b]].Ru = [[a.cosA-b.sinA],[a.sinA+b.cosA]]
           this is for 2D vector, for 3D and up, use this matrix respectively on 2 axes and keep other coorinate like before
        
        2D: (a1,a2).Ru=(a1u,a2u)
        3D: (a1,a2,a3) => (a2,a3).Ru1    =via 2D=(a2u1,a3u1),
                          (a1,a3u1).Ru2  =via 2D=(a1u2,a3u1u2),
                          (a1u2,a2u1).Ru3=via 2D=(a1u2u3,a2u1u3)
            (a1u2u3,a2u1u3,a3u1u2) <=
        4D: (a1,a2,a3,a4) => (a2,a3,a4).Ru1            =via 3D=(a2u1,a3u1,a4u1),
                             (a1,a3u1,a4u1).Ru2        =via 3D=(a1u2,a3u1u2,a4u1u2),
                             (a1u2,a2u1,a4u1u2).Ru3    =via 3D=(a1u2u3,a2u1u3,a4u1u2u3)
                             (a1u2u3,a2u1u3,a3u1u2).Ru4=via 3D=(a1u2u3u4,a2u1u3u4,a3u1u2u4)
            (a1u2u3u4,a2u1u3u4,a3u1u2u4,a4u1u2u3) <=
        '''
        pdb.set_trace()
        if V==None: V=self.vectorList

        if angleUnit == 'deg':
            for i in range(len(angles)):
                angles[i]=math.radians(float(angles[i]))

        #TODO
        #finalize rotation
         
        if dim==1:
            Vrot=list()
            for i in range(len(V)):
                newCoord=(V[i].coord[0]*math.cos(angles[0])-V[i].coord[1]*math.sin(angles[0]),V[i].coord[0]*math.sin(angles[0])+V[i].coord[1]*math.cos(angles[0]))
                if i==0: Porigin = V[i].origin
                else:    Porigin = V[i].translat(Vrot[i-1].end).origin
                Vrot.append(Vector(Porigin,newCoord))

        #for dim>=3
        #dim=len(angles)
        #    Vrot=list(V)
        #    for i in range(len(angles)):
        #        Vreduce=list(V)
        #        Vreduce.pop(i)
        #        Vreduce = self.rotate(list(angles[0]),V=Vreduce)
        #        for j in range(len(Vrot)):
        #            if j!=i:
        #                for k in range(len(Vreduce)):
        #                    Vrot[j+k]=Vreduce[k]
        return Vrot
                  
            

    def isInShadow(self,Ptest,Porigin=None,online=True):
        #pdb.set_trace()
        if Porigin==None: Porigin=self.pointList[0]

        if Porigin in self.pointList and self.pointList[0]!=Porigin:
            self.turn(Porigin)

        self.orientate(1)

        inshadow=list([self.vectorList[0].isRight(Ptest,online)])
        for i in range(1,len(self.vectorList)-1):
            inshadow.append(self.vectorList[i].isLeft(Ptest,online))
        inshadow.append(self.vectorList[len(self.vectorList)-1].isRight(Ptest,online))

        n=0
        for i in range(len(inshadow)):
            if inshadow[i]:
                n+=1

        return n == len(inshadow)

        
    def isInPolygon(self,Ptest,Porigin=None,online=True):
        if Porigin==None: Porigin=self.pointList[0]

        if Porigin in self.pointList and self.pointList[0]!=Porigin:
            self.turn(Porigin)

        self.orientate(1)

        n=0
        for v in self.vectorList:
            if v.isRight(Ptest,online):
                n+=1

        return n==len(self.vectorList)
        

# area3D_Polygon(): compute the area of a 3D planar polygon
#  Input:  int n = the number of vertices in the polygon
#          Point* V = an array of n+1 points in a 2D plane with V[n]=V[0]
#          Point N = a normal vector of the polygon's plane
#  Return: the (float) area of the polygon
def area3D_Polygon(n, Plist, N):
    import math

    area = 0;

    if n < 3: return 0  # a degenerate polygon

    # select largest abs coordinate to ignore for projection
    if N.x>0: ax=N.x   # abs x-coord
    else:     ax=-N.x
    if N.y>0: ay=N.y   # abs y-coord
    else:     ay=-N.y
    if N.z>0: az=N.z   # abs z-coord
    else:     az=-N.z  

    coord = 3;                          # ignore z-coord
    if ax > ay and ax > az: coord = 1   # ignore x-coord
    elif ay > az: coord = 2             # ignore y-coord

    # compute area of the 2D projection
    if coord == 1:
        j=2
        k=0
        for i in range(1,n+1):
            area += (Plist[i].y * (Plist[j].z - Plist[k].z))
            j+=1
            k+=1

    elif coord == 2:
        j=2
        k=0
        for i in range(1,n+1):
            area += (Plist[i].z * (Plist[j].x - Plist[k].x))
            j+=1
            k+=1

    elif coord == 3:
        j=2
        k=0
        for i in range(1,n+1):
            area += (Plist[i].x * (Plist[j].y - Plist[k].y))
            j+=1
            k+=1

    # wrap-around term
    if coord == 1:
        area += (Plist[n].y * (Plist[1].z - Plist[n-1].z))
    elif coord == 2:
        area += (Plist[n].z * (Plist[1].x - Plist[n-1].x))
    elif coord == 3:
        area += (Plist[n].x * (Plist[1].y - Plist[n-1].y))

    # scale to get area before projection
    an = math.sqrt( ax*ax + ay*ay + az*az); # length of normal vector
    if coord == 1:
        area *= (an / (2 * N.x))
    elif coord == 2:
        area *= (an / (2 * N.y))
    elif coord == 3:
        area *= (an / (2 * N.z))

    return area


pdb.set_trace()
P2_0 = Point(0,0)
P2_11 = Point(-1,1)
P2_12 = Point(-1,2)

P2_2 = Point(-2,2)
P2_3 = Point(-3,2)
P2_4 = Point(-2,3)
P2_5 = Point(-1,3)

P3_0 = Point(0,0,0)
P3_11 = Point(-2,2,0)
P3_12 = Point(2,2,0)
P3_13 = Point(1,0,2)


print("P2_0:  {}".format(P2_0))
print("P2_11: {}".format(P2_11))
print("P2_12: {}".format(P2_12))

print("P3_0:  {}".format(P3_0))
print("P3_11: {}".format(P3_11))
print("P3_12: {}".format(P3_12))
print("P3_13: {}".format(P3_13))

print("Vector(P2_0,P2_11):        {}".format(Vector(P2_0,P2_11)))
print("Vector((1,2)):             {}".format(Vector((1,2))))
print("Vector(P2_0,(1,2)):        {}".format(Vector(P2_0,(1,2))))
print("Vector(1,(90,'deg')):      {}".format(Vector(1,(90,'deg'))))
print("Vector(P2_0,1,(90,'deg')): {}".format(Vector(P2_0,1,(90,'deg'))))

print("Vector(origin=P2_0,end=P2_11): {}".format(Vector(origin=P2_0,end=P2_11)))
print("Vector(coord=(1,2)): {}".format(Vector(coord=(1,2))))
print("Vector(orig=P2_0,coord=(1,2)): {}".format(Vector(orig=P2_0,coord=(1,2))))
print("Vector(norme=1,angle=(90,'deg')): {}".format(Vector(norme=1,angle=(90,'deg'))))
print("Vector(orig=P2_0,norme=1,angle=(90,'deg')):{}".format(Vector(orig=P2_0,norme=1,angle=(90,'deg'))))

print("Vector(P2_0,end=P2_11): {}".format(Vector(P2_0,end=P2_11)))
print("Vector(P2_0,coord=(1,2)): {}".format(Vector(P2_0,coord=(1,2))))
print("Vector(1,angle=(90,'deg')): {}".format(Vector(1,angle=(90,'deg'))))
print("Vector(P2_0,1,angle=(90,'deg')): {}".format(Vector(P2_0,1,angle=(90,'deg'))))

print("Vector(P2_0,P2_11): {}".format(Vector(P2_0,P2_11)))
print("Vector(P2_0,P2_12): {}".format(Vector(P2_0,P2_12)))
print("Vector(P2_11,P2_12): {}".format(Vector(P2_11,P2_12)))
print("Vector(P2_12,P2_11): {}".format(Vector(P2_12,P2_11)))
print("polygon2D([P2_0,P2_11,P2_12]).orientation(): {}".format(polygon2D([P2_0,P2_11,P2_12]).orientation()))

print Vector(P2_0,Point(1,2))
print Vector(P2_0,Point(3,2))
print Vector(Point(1,2),Point(3,2))
print Vector(Point(3,2),Point(1,2))
print("polygon2D([P2_0,Point(1,2),Point(3,2)]).orientation(): {}".format(polygon2D([P2_0,Point(1,2),Point(3,2)]).orientation()))

print Vector(P2_0,Point(2,-1))
print Vector(P2_0,Point(0,-1))
print Vector(Point(2,-1),Point(0,-1))
print Vector(Point(0,-1),Point(2,-1))
print("polygon2D([P2_0,Point(2,-1),Point(0,-1)]).orientation(): {}".format(polygon2D([P2_0,Point(2,-1),Point(0,-1)]).orientation()))

print Vector(P2_0,Point(-2,-1))
print Vector(P2_0,Point(-2,-2))
print Vector(Point(-2,-1),Point(-2,-2))
print Vector(Point(-2,-2),Point(-2,-1))
print("polygon2D([P2_0,Point(-2,-1),Point(-2,-2)]).orientation(): {}".format(polygon2D([P2_0,Point(-2,-1),Point(-2,-2)]).orientation()))

print("Is P2_2 ({}) in shadow of polygon2D([P2_0,P2_11,P2_12]) from origin P2_0 ({}): {}".format(P2_2,P2_0,polygon2D([P2_0,P2_11,P2_12]).isInShadow(P2_2)))
print("Is P2_3 ({}) in shadow of polygon2D([P2_0,P2_11,P2_12]) from origin P2_0 ({}): {}".format(P2_3,P2_0,polygon2D([P2_0,P2_11,P2_12]).isInShadow(P2_3)))
print("Is P2_4 ({}) in shadow of polygon2D([P2_0,P2_11,P2_12]) from origin P2_0 ({}): {}".format(P2_4,P2_0,polygon2D([P2_0,P2_11,P2_12]).isInShadow(P2_4)))
print("Is P2_5 ({}) in shadow of polygon2D([P2_0,P2_11,P2_12]) from origin P2_0 ({}): {}".format(P2_5,P2_0,polygon2D([P2_0,P2_11,P2_12]).isInShadow(P2_5)))
print("Is {} in shadow of polygon2D([P2_0,P2_11,P2_12]) from origin P2_0 ({}): {}".format(Point(-3,3),P2_0,polygon2D([P2_0,P2_11,P2_12]).isInShadow(Point(-3,3))))

print ""
print("Is {} in shadow of polygon2D([P2_0,Point(1,2),Point(3,2)]) from origin P2_0 ({}): {}".format(Point(1,1),P2_0,polygon2D([P2_0,Point(1,2),Point(3,2)]).isInShadow(Point(1,1))))
print("Is {} in shadow of polygon2D([P2_0,Point(1,2),Point(3,2)]) from origin P2_0 ({}): {}".format(Point(2,1),P2_0,polygon2D([P2_0,Point(1,2),Point(3,2)]).isInShadow(Point(2,1))))
print("Is {} in shadow of polygon2D([P2_0,Point(1,2),Point(3,2)]) from origin P2_0 ({}): {}".format(Point(3,1),P2_0,polygon2D([P2_0,Point(1,2),Point(3,2)]).isInShadow(Point(3,1))))
print("Is {} in shadow of polygon2D([P2_0,Point(1,2),Point(3,2)]) from origin P2_0 ({}): {}".format(Point(1,3),P2_0,polygon2D([P2_0,Point(1,2),Point(3,2)]).isInShadow(Point(1,3))))
print("Is {} in shadow of polygon2D([P2_0,Point(1,2),Point(3,2)]) from origin P2_0 ({}): {}".format(Point(2,3),P2_0,polygon2D([P2_0,Point(1,2),Point(3,2)]).isInShadow(Point(2,3))))
print("Is {} in shadow of polygon2D([P2_0,Point(1,2),Point(3,2)]) from origin P2_0 ({}): {}".format(Point(3,3),P2_0,polygon2D([P2_0,Point(1,2),Point(3,2)]).isInShadow(Point(3,3))))
print("Is {} in shadow of polygon2D([P2_0,Point(1,2),Point(3,2)]) from origin P2_0 ({}): {}".format(Point(4,3),P2_0,polygon2D([P2_0,Point(1,2),Point(3,2)]).isInShadow(Point(4,3))))
print("Is {} in shadow of polygon2D([P2_0,Point(1,2),Point(3,2)]) from origin P2_0 ({}): {}".format(Point(5,3),P2_0,polygon2D([P2_0,Point(1,2),Point(3,2)]).isInShadow(Point(5,3))))


print ""
print polygon2D([P2_0,P2_11,P2_12]).rotate([90],'deg')









