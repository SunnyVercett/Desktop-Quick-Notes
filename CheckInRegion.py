#! /usr/bin/env python
#coding=utf-8

# cast a ray from p to the left and right, check its intersects with the polygon
# has odd numbers of intersects on the left of p, and odd numbers of intersects on the right of p

import math

global x,y
x = 0    # scale on x-axis
y = 1    # scale on y-axis

class CoordinateNotDigitException(Exception):
    pass

class CoincidedPointsException(Exception):
    pass

class VerticalLineException(Exception):
    pass

class HorizontalLineException(Exception):
    pass

class PolygonVertexNotCompleteException(Exception):
    pass

class NoIntersectError(Exception):
    pass

class GeometryTypeError(Exception):
    pass

class PlaneGeometryComponent(object):    # the visual class for geometry objects
    pass


class Point2D(PlaneGeometryComponent):
    x = 0
    y = 0
    
    def __init__(self,x,y):    # receive two floats
        if (type(x)!=type(0)) and (type(x)!=type(0.0)):
            raise CoordinateNotDigitException("Invalid parameter type for the x-coordinate to construct a point.")
        if (type(y)!=type(0)) and (type(y)!=type(0.0)):
            raise CoordinateNotDigitException("Invalid parameter type for the y-coordinate to construct a point.")
        self.x = x
        self.y = y
        
    def __eq__(self,other):    # receive a point2d object
        if not isinstance(other,Point2D):
            raise GeometryTypeError("A non-point object encountered when trying to determine equivalence of two points.")
        
        return (other.x==self.x) and (other.y==self.y)
        
        
class Segment2D(PlaneGeometryComponent):
    startPoint = Point2D(0,0)
    endPoint = Point2D(0,0)
    slope = 0
    xIntercept = 0
    yIntercept = 0
    
    def __init__(self,p1,p2):    # receive two point2d objects
        if p1==p2:
            raise CoincidedPointsException("The two points have the same coordinates. Cannot construct a line.")
        
        self.startPoint = p1
        self.endPoint = p2
        
        if self.startPoint.y==self.endPoint.y:    # vertical segment
            self.slope = 0
            self.xIntercept = None
            self.yIntercept = 1.0*self.startPoint.y
        elif self.startPoint.x==self.endPoint.x:    # horizontal segment
            self.slope = None
            self.xIntercept = 1.0*self.startPoint.x
            self.yIntercept = None
        else:
            self.slope = (self.endPoint.y*1.0-self.startPoint.y)/(self.endPoint.x*1.0-self.startPoint.x)
            self.yIntercept = self.startPoint.y-self.slope*self.startPoint.x
            self.xIntercept = 0-(1.0/self.slope)*self.yIntercept
            
            
    def __eq__(self,other):
        if not isinstance(other,Segment2D):
            raise GeometryTypeError("A non-segment object encountered when trying to determine equivalence of two segments.")
        
        return (self.startPoint==other.startPoint and self.endPoint==other.endPoint)
            
            
class Polygon2D(PlaneGeometryComponent):
    vertexList = []
    edgeList = []
    
    def __init__(self,pList):    # receive a list of floats (each pair represents coordinates of a point), or a list of tuples or lists, or a list of point objects
        # receive a list of floats, the count of which must be even
        if isinstance(pList[0],int) or isinstance(pList[0],float):
            if len(pList)&1 or len(pList)<6:    # length of the list is a odd number, or less than 6 (meaning less than 3 points)
                raise PolygonVertexNotCompleteException("Cannot construct a polygon from the parameters.")
            
            lastVertex = None
            for eachFloatIndex in xrange(0,len(pList),2):
                thisVertex = Point2D(pList[eachFloatIndex],pList[eachFloatIndex+1])    # convert these two floats to a point object
                self.vertexList += [thisVertex]
                if lastVertex:
                    if thisVertex==lastVertex:
                        continue    # skip overlapped points
                    thisEdge = Segment2D(lastVertex,thisVertex)    # in this case the last edge will not join into the edgeList
                    self.edgeList += [thisEdge]
                lastVertex = thisVertex
            
            finalVertex = Point2D(pList[-2],pList[-1])
            firstVertex = Point2D(pList[0],pList[1])
            finalEdge = Segment2D(finalVertex,firstVertex)
            self.edgeList += [finalEdge]    # fill on the final edge that goes from the final vertex to the first vertex
        
        # receive a list of tuple or list, each represent a point
        elif isinstance(pList[0],tuple) or isinstance(pList[0],list):
            if len(pList)<3:    # length of the list is less than 3
                raise PolygonVertexNotCompleteException("Cannot construct a polygon from the parameters.")
            
            lastVertex = None
            for eachPoint in pList:
                thisVertex = Point2D(eachPoint[0],eachPoint[1])    # convert this tuple or list representing a point to a point object
                self.vertexList += [thisVertex]
                if lastVertex:
                    if thisVertex==lastVertex:
                        continue    # skip overlapped points
                    thisEdge = Segment2D(lastVertex,thisVertex)
                    self.edgeList += [thisEdge]
                lastVertex = thisVertex
                
            finalVertex = Point2D(pList[-1][0],pList[-1][1])
            firstVertex = Point2D(pList[0][0],pList[0][1])
            finalEdge = Segment2D(finalVertex,firstVertex)
            self.edgeList += [finalEdge]    # fill on the final edge that goes from the final vertex to the first vertex
            
        # receive a list of point objects
        elif isinstance(pList[0],Point2D):
            if len(pList)<3:
                raise PolygonVertexNotCompleteException("Cannot construct a polygon from the parameters.")
                
            lastVertex = None
            for eachPoint in pList:
                self.vertexList += [eachPoint]
                if lastVertex:
                    if eachPoint==lastVertex:
                        continue    # skip overlapped points
                    thisEdge = Segment2D(lastVertex,thisVertex)
                    self.edgeList += [thisEdge]
                lastVertex = thisVertex
                
            finalEdge = Segment2D(pList[-1],pList[0])
            self.edgeList += [finalEdge]    # fill on the final edge that goes from the final vertex to the first vertex
                
                
    def __eq__(self,other):
        if not isinstance(other,Polygon2D):
            raise GeometryTypeError("A non-polygon object encountered when trying to determine equivalence of two polygons.")
        
        condition = 0
        for eachVertex in self.vertexList:
            if eachVertex not in other.vertexList:
                condition += 1    # each vertex in this polygon is in the other polygon
        for eachVertex in other.vertexList:
            if eachVertex not in self.vertexList:
                condition += 1    # each vertex in the other polygon is in self polygon
                
        return (not condition)
        

def isInSegment(p,e):
    '''To determine whether a point is on a line segment. Endpoint of the segment included.'''
    
    if not isinstance(p,Point2D):
        raise GeometryTypeError("A non-point object encountered in function 'isInSegment()'.")
    if not isinstance(e,Segment2D):
        raise GeometryTypeError("A non-segment object encountered in function 'isInSegment()'.")
    
    # the segment is vertical or horizontal
    if e.slope==0:    # horizontal
        return p.y==e.startPoint.y and (e.startPoint.x<=p.x<=e.endPoint.x or e.endPoint.x<=p.x<=e.startPoint.x)
    elif e.slope==None:    # vertical
        return p.x==e.startPoint.x and (e.startPoint.y<=p.y<=e.endPoint.y or e.endPoint.y<=p.y<=e.startPoint.y)
    
    # other circumstances
    condition1 = ((e.endPoint.x-p.x)/(p.x-e.startPoint.x)==(e.endPoint.y-p.y)/(p.y-e.startPoint.y))    # this point is on the line in which the segment exists
    
    minX = min(e.startPoint.x,e.endPoint.x)
    maxX = max(e.startPoint.x,e.endPoint.x)
    minY = min(e.startPoint.y,e.endPoint.y)
    maxY = max(e.startPoint.y,e.endPoint.y)
    condition2 = (minX<=p.x<=maxX and minY<=p.y<=maxY)
            
    return condition1 and condition2


def getIntersect_horizontal(p,e):
    '''Get the intersect of a horizontal line through the point p and another line.'''
    
    if not isinstance(p,Point2D):
        raise GeometryTypeError("A non-point object encountered in function 'isInSegment()'.")
    if not isinstance(e,Segment2D):
        raise GeometryTypeError("A non-segment object encountered in function 'isInSegment()'.")
    
    if e.slope==0:
        raise HorizontalLineException("This line is horizontal. No intersect can be found.")
    
    minY = min(e.startPoint.y,e.endPoint.y)
    maxY = max(e.startPoint.y,e.endPoint.y)
    if minY>p.y or maxY<p.y:
        raise NoIntersectError("No intersect between horizontal line through this point and the segment.")
    
    if p.y==e.startPoint.y:
        return e.startPoint    # the intersect is the start point of the segment
    
    if e.yIntercept:    # has a valid y-axis intercept
        return Point2D((p.y-e.yIntercept)/e.slope,p.y)
    else:
        return Point2D(e.startPoint.x,p.y)


def getIntersect_vertical(p,e):
    '''Get the intersect of a vertical line through the point p and another line.'''
    
    if not isinstance(p,Point2D):
        raise GeometryTypeError("A non-point object encountered in function 'isInSegment()'.")
    if not isinstance(e,Segment2D):
        raise GeometryTypeError("A non-segment object encountered in function 'isInSegment()'.")
    
    if e.slope==None:
        raise VerticalLineException("This line is vertical. No intersect can be found.")
    
    minX = min(e.startPoint.x,e.endPoint.x)
    maxX = max(e.startPoint.x,e.endPoint.x)
    if minX>p.x or maxX<p.x:
        raise NoIntersectError("No intersect between vertical line through this point and the segment.")
    
    if p.x==e.startPoint.x:
        return e.startPoint    # the intersect is the start point of the segment
    
    return Point2D(p.x,e.yIntercept+e.slope*p.x)


def isInPolygon(p,polygon):
    '''To determine whether a point is in a polygon, including its edge.'''
    
    if not isinstance(p,Point2D):
        raise GeometryTypeError("A non-point object encountered in function 'isInPolygon()'.")
    if not isinstance(polygon,Polygon2D):
        raise GeometryTypeError("A non-polygon object encountered in function 'isInPolygon()'.")
    
    intersectsUp = 0
    intersectsDown = 0
    intersectsRight = 0
    intersectsLeft = 0
    
    for thisVertex in polygon.vertexList:
        if thisVertex==p:
            return True
        else:
            if thisVertex.x==p.x:
                if thisVertex.y<p.y:
                    intersectsDown += 1
                else:
                    intersectsUp += 1    # y displace could not be equal, so "else" statement is good
            elif thisVertex.y==p.y:    # x displace and y displace could only be equal for one, otherwise it goes in the above block, so "elif" is good
                if thisVertex.x<p.x:
                    intersectsLeft += 1
                else:
                    intersectsRight += 1
    
    for thisEdge in polygon.edgeList:     # segments of the polygon one by one   
        if isInSegment(p,thisEdge):    # if this point is on the edge of the polygon
            return True
        
        if (thisEdge.startPoint.y-p.y)*(thisEdge.endPoint.y-p.y) < 0:    # cast a horizontal line
            if thisEdge.slope==0:    # this edge is horizontal. only happens if the edge is on the horizontal line, in which case there are infinite intersects
                intersect = None    # then the start point of the edge is counted as the only intersect
            else:
                if p.y==thisEdge.endPoint.y:    # exclude end point of each edge, to avoid repeat
                    intersect = None
                else:
                    intersect = getIntersect_horizontal(p,thisEdge)
                    
            if intersect:    # the horizontal line through this point has an intersect with this edge
                if intersect.x<p.x:
                    intersectsLeft += 1
                else:
                    intersectsRight += 1
                
        if (thisEdge.startPoint.x-p.x)*(thisEdge.endPoint.x-p.x) <= 0:    # cast a vertical line
            if thisEdge.slope==None:    # this edge is vertical. only happens if the edge is on the vertical line, in which case there are infinite intersects
                intersect = e.startPoint    # then the start point of the edge is counted as the only intersect
            else:
                if p.x==thisEdge.endPoint.x:    # exclude end point of each edge, to avoid repeat
                    intersect = None
                else:
                    intersect = getIntersect_vertical(p,thisEdge)
                
            if intersect:
                if intersect.y<p.y:
                    intersectsDown += 1
                else:
                    intersectsUp += 1
                
    c1 =  intersectsUp&1 and intersectsDown&1 and intersectsLeft&1 and intersectsRight&1
    return bool(c1),intersectsUp,intersectsDown,intersectsLeft,intersectsRight
    
    
# in progress
#def getDistance(p,p1,p2):
#    '''calculate the distance between a line and a dot'''
#    p[x] = float(p[x])
#    p[y] = float(p[y])
#    p1[x] = float(p1[x])
#    p1[y] = float(p1[y])
#    p2[x] = float(p2[x])
#    p2[y] = float(p2[y])
#    
#    if p1[y]==p2[y]:
#        return abs(p1[y]-p[y])
#    elif p1[x]==p2[x]:
#        return abs(p1[x]-p[x])
#    else:
#        k = float((p2[y]-p1[y]))/float((p2[x]-p1[x]))
#        _k = -1.0/k
#        _p = ()
#        # p0 is the intersect of the target line and the line vertical to the target line and through the targetpoint




if __name__=='__main__':
    p1 = Point2D(2,3)
    p2 = Point2D(3,4)
    p3 = Point2D(2,3)
    print p1==p2
    print p1==p3
    
    seg = Segment2D(p1,p2)
    print seg.yIntercept
    
    p4 = Point2D(2.5,3.5)
    print isInSegment(p4,seg)
    
    p5 = Point2D(2.5,4.5)
    intersect = getIntersect_vertical(p5,seg)
    print intersect.x,intersect.y
    
    p6 = Point2D(3.5,3.5)
    intersect2 = getIntersect_horizontal(p6,seg)
    print intersect2.x,intersect2.y
    
    l = [1,0,0,1,-1,0,0,-1]
    #p71 = Point2D(2,0)
    #p72 = Point2D(0,0)
    #seg = Segment2D(p71,p72)
    polygon = Polygon2D(l)
    p7 = Point2D(0,0)
    #intersectsDown = getIntersect_vertical(p7,seg)
    #print intersectsDown.x,intersectsDown.y
    print isInPolygon(p7,polygon)
