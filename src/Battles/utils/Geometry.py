"""
Created on Apr 17, 2013

@author: Albert Mas
"""
import Message
import math
import Polygon
import Polygon.Utils
from random import random, uniform

PI = 3.14159265359


class Point2D:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y
        self.data = None  # Useful when a point have to carry any kind of data (by example, to identify different type of points used in geometry algorithms)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def Copy(self):
        p = Point2D(self.x, self.y)
        return p

    def SetFrom3D(self, p3d):
        self.x = p3d.x
        self.y = p3d.y
        return self

    def Distance(self, point):
        # Returns the distance between current point and given one
        # return math.sqrt(((self.x - point.x)**2) + ((self.y - point.y)**2))
        return math.hypot(self.x - point.x, self.y - point.y)

    def Move(self, vector, offset):
        # Moves the point along given vector and with given offset
        self.x = self.x + (offset * vector.val[0])
        self.y = self.y + (offset * vector.val[1])

    def GetMove(self, vector, offset):
        # Like Move metho, but modifying only a new returned object
        p = self.Copy()
        p.x = p.x + (offset * vector.val[0])
        p.y = p.y + (offset * vector.val[1])
        return p

    def MoveAngle(self, angle, offset):
        # Like move, but with a degree angle
        rad = math.radians(angle)
        self.x += offset * math.cos(rad)
        self.y += offset * math.sin(rad)

    def Sum(self, point):
        # Sums the point coordinates
        self.x = point.x
        self.y = point.y
        return self

    def Div(self, scalar):
        # Divides all coordinate values by given scalar
        if (scalar == 0):
            return self
        else:
            self.x /= scalar
            self.y /= scalar
            return self

    def IsInCircle(self, center, radius):
        if (self.Distance(center) < radius):
            return True
        else:
            return False

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __str__(self):
        return "[{}, {}]".format(self.x, self.y)


class Point3D:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "[{}, {}, {}]".format(self.x, self.y, self.z)

    def Copy(self):
        p = Point3D(self.x, self.y, self.z)
        return p

    def SetFrom2D(self, p2d):
        self.x = p2d.x
        self.y = p2d.y
        self.z = 0
        return self

    def Distance(self, point):
        # Returns the distance between current point and given one
        return math.sqrt(((self.x - point.x) ** 2) + ((self.y - point.y) ** 2) + ((self.z - point.z) ** 2))

    def Move(self, vector, offset):
        # Moves the point along given vector and with given offset
        self.x = self.x + (offset * vector.val[0])
        self.y = self.y + (offset * vector.val[1])
        self.z = self.z + (offset * vector.val[2])

    def GetString(self):
        return '[' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ']'

    def Sum(self, point):
        # Sums the point coordinates
        self.x += point.x
        self.y += point.y
        self.z += point.z
        return self

    def Div(self, scalar):
        # Divides all coordinate values by given scalar
        if (scalar == 0):
            return self
        else:
            self.x /= scalar
            self.y /= scalar
            self.z /= scalar
            return self


class Vector2D:
    def __init__(self, x=0.0, y=0.0):
        self.val = [x, y]

    def Copy(self):
        v = Vector2D(self.val[0], self.val[1])
        return v

    def SetFrom3D(self, v3d):
        self.val[0] = v3d.val[0]
        self.val[1] = v3d.val[1]

        return self

    def Invert(self):
        self.val[0] = -self.val[0]
        self.val[1] = -self.val[1]

        return self

    def IsNull(self):
        if ((self.val[0] == 0) and (self.val[1] == 0)):
            return True
        else:
            return False

    def Random(self):

        # seed()

        self.val[0] = 0.0
        self.val[1] = 0.0
        while ((self.val[0] == 0.0) and (self.val[1] == 0.0)):
            self.val[0] = uniform(-1.0, 1.0)
            self.val[1] = uniform(-1.0, 1.0)

        self.Normalize()
        return self

    def CreateFrom2Points(self, p1, p2, normalize=True):
        if (not p1 or not p2):
            a = 1
            return self

        self.val[0] = p2.x - p1.x
        self.val[1] = p2.y - p1.y
        if (normalize):
            self.Normalize()

        return self

    def Module(self):
        # return math.sqrt((self.val[0]**2) + (self.val[1]**2))
        return math.hypot(self.val[0], self.val[1])

    def module_2(self):
        return self.val[0]*self.val[0] + self.val[1]*self.val[1]

    def Normalize(self):
        l = self.Module()
        if (l == 0):
            self.val[0] = 0
            self.val[1] = 0
        else:
            self.val[0] /= l
            self.val[1] /= l

        return self

    def DotProd(self, v):
        return (self.val[0] * v.val[0]) + (self.val[1] * v.val[1])

    def CrossProd(self, v):
        return self.Det(v)

    def Det(self, v):
        return (self.val[0] * v.val[1]) - (self.val[1] * v.val[0])

    def Rotate(self, deg):

        rad = math.radians(deg)

        c = math.cos(rad)
        s = math.sin(rad)

        x = (self.val[0] * c) - (self.val[1] * s)
        y = (self.val[0] * s) - (self.val[1] * c)
        self.val[0] = x
        self.val[1] = y

    def GetAngle(self):
        # Return the angle (degrees) related to current vector (polar to rectangle coordinates)

        if (self.val[0] == 0.0):
            if (self.val[1] > 0.0):
                return 90.0
            else:
                return 270.0
        else:
            ang = math.atan2(self.val[1], self.val[0])
            return math.degrees(ang)

    def AngleBetween(self, v):
        # Returns the 2D angle between current and given vector    
        # rad = math.acos(self.DotProd(v))
        dotprod = (self.val[0] * v.val[0]) + (self.val[1] * v.val[1])
        if (dotprod > 1):
            dotprod = 1
        elif (dotprod < -1):
            dotprod = -1
        rad = math.acos(dotprod)
        return math.degrees(rad)

    def Bisector(self, v):
        # Returns the bisector vector between current and given vectors
        l1 = self.Module()
        l2 = v.Module()

        bis = Vector2D()
        bis.val[0] = (l1 * v.val[0]) + (l2 * self.val[0])
        bis.val[1] = (l1 * v.val[1]) + (l2 * self.val[1])
        bis.Normalize()

        return bis

    def GetPerpendicular(self):
        # Returns the perpendicular vector
        v = Vector2D()
        v.val[0] = -self.val[1]
        v.val[1] = self.val[0]
        return v


class Segment2D():

    def __init__(self, p1=Point2D(), p2=Point2D()):
        self.p1 = p1
        self.p2 = p2

    def Copy(self):
        return Segment2D(self.p1.Copy(), self.p2.Copy())

    def GetLength(self):
        return self.p1.Distance(self.p2)

    def DistanceToPoint(self, p, squared=False):
        # Returns the distance from given point to current segment
        # Returns -1 if segment is too short

        seglen = self.GetLength()
        if (seglen < 0.00000001):
            return -1

        # Calculates the projection of current point over line
        # Calculates the percentage position of current point over segment
        # Consider the two vectors from current point to segment vertices. Then perform the dot product, and divide it by square length
        r = (((p.x - self.p1.x) * (self.p2.x - self.p1.x)) + ((p.y - self.p1.y) * (self.p2.y - self.p1.y))) / (
                    seglen ** 2)

        if ((r < 0.00001) or (r > 1)):
            # The projection doesnt fall over segment. Get the shortest distance to the segment vertices
            if (not squared):
                # d1 = p.Distance(self.p1)
                d1 = math.hypot(self.p1.x - p.x, self.p1.y - p.y)
                # d2 = p.Distance(self.p2)
                d2 = math.hypot(self.p2.x - p.x, self.p2.y - p.y)
                return min(d1, d2)

            else:
                d1 = (self.p1.x - p.x) ** 2 + (self.p1.y - p.y) ** 2
                d2 = (self.p2.x - p.x) ** 2 + (self.p2.y - p.y) ** 2
                return min(d1, d2)

        else:
            # Calculate the projection point
            prj = Point2D(self.p1.x + r * (self.p2.x - self.p1.x), self.p1.y + r * (self.p2.y - self.p1.y))

            # Get the distance between projection point and current one
            if (not squared):
                # return p.Distance(prj)
                return math.hypot(prj.x - p.x, prj.y - p.y)
            else:
                return ((prj.x - p.x) ** 2 + (prj.y - p.y) ** 2)

    def ProjectPoint(self, point, forceprojection=False):
        # Returns the projection of given point over segment
        # If projection falls over the segment bounds, move to closest segment vertex
        # Returns None if segment is  too short
        # If forceprojection is true, returns None if projection point falls out of segment

        p = point

        seglen = self.GetLength()
        if (seglen < 0.00000001):
            return None

        # Calculates the projection of current point over line
        # Calculates the percentage position of current point over segment
        # Consider the two vectors from current point to segment vertices. Then perform the dot product, and divide it by square length
        r = (((p.x - self.p1.x) * (self.p2.x - self.p1.x)) + ((p.y - self.p1.y) * (self.p2.y - self.p1.y))) / (
                    seglen ** 2)

        if ((r < 0.00001) or (r > 1)):

            if (forceprojection):
                return None
            else:
                # The projection doesnt fall out of segment. Get the shortest distance to the segment vertices
                d1 = p.Distance(self.p1)
                d2 = p.Distance(self.p2)
                if (d1 >= d2):
                    return self.p2
                else:
                    return self.p1

        else:
            # Calculate the projection point
            return Point2D(self.p1.x + r * (self.p2.x - self.p1.x), self.p1.y + r * (self.p2.y - self.p1.y))

    def GetNormal(self):
        # Returns the normal 2D vector of current segment 
        # From the two possible normal vectors, it returns the "under-segment" one

        v = Vector2D().CreateFrom2Points(self.p2, self.p1, True)
        return v.GetPerpendicular()

    def GetDirection(self):

        v = Vector2D().CreateFrom2Points(self.p1, self.p2, True)
        return v

    def AngleBetween(self, seg):
        # Return the angle between segments
        v1 = self.GetDirection()
        v2 = seg.GetDirection()
        return v1.AngleBetween(v2)

    def GetMidPoint(self):

        v = Vector2D().CreateFrom2Points(self.p1, self.p2)
        m = self.p1.Copy()
        m.Move(v, self.GetLength() / 2.0)

        return m

    def ConvexTo(self, seg):
        # Returns true if the sequence of current and given segment gives a convex join

        v = Vector2D().CreateFrom2Points(self.p1, seg.p2)
        if (self.GetDirection().Det(v) >= 0):
            return True
        else:
            return False

    def Move(self, direction, distance):
        # Move the segment at given direction and at given distance
        self.p1.Move(direction, distance)
        self.p2.Move(direction, distance)

    def GetBounding(self, margin):
        # Returns a polygon around current segment with given margin

        # The simplest way (but less elegant) is to create two segments from vertices and to extend them by margin value. Then, create two segments more to join the first ones

        nvec = self.GetNormal()
        nvecinv = self.GetNormal().Invert()

        sleft = Segment2D(p1=self.p1.Copy(), p2=self.p1.Copy())
        sleft.p1.Move(nvec, margin)
        sleft.p2.Move(nvecinv, margin)

        sright = Segment2D(p1=self.p2.Copy(), p2=self.p2.Copy())
        sright.p2.Move(nvec, margin)
        sright.p1.Move(nvecinv, margin)

        poly = Polygon2D()
        poly.shape.append(sleft)
        poly.shape.append(Segment2D(p1=sleft.p1, p2=sright.p2))
        poly.shape.append(sright)
        poly.shape.append(Segment2D(p1=sright.p1, p2=sleft.p2))

        return poly

    def Intersect(self, segment, margin=0, onlycheck=False):
        # Returns the intersection point between segments (or None if they dont intersect)
        # If margin is >0, the algorithm consider a bounding rectangle around each segment
        # If onlycheck is True only returns if there is any intersection (faster)
        # WARNING: If margin is >0, onlycheck has to be true, due we use rectangles around the segments, and two rectangles can intersect in its area, but not necessarily in their sides

        if ((margin > 0) and not onlycheck):
            print "WARNING: Cannot check the intersection point between two rectangles, just knowing if there are any intersection. Checking without margin"
            margin = 0

        if (margin > 0):
            poly1 = self.GetBounding(margin)
            poly2 = segment.GetBounding(margin)

            return poly1.Intersect(poly2)

        # Get the line equations for each segment and solve them

        # Special cases
        if (((self.p1.x - self.p2.x) == 0) and ((segment.p1.x - segment.p2.x) == 0)):
            return None  # parallel vertical lines
        elif ((self.p1.x - self.p2.x) == 0):
            # Current segment is vertical

            # Now, a nice self way to get the intersection. Critics are allowed ...

            # Discard outofbounds cases
            if ((max(segment.p1.x, segment.p2.x) < self.p1.x) or (min(segment.p1.x, segment.p2.x) > self.p1.x)):
                return None
            if ((max(segment.p1.y, segment.p2.y) < min(self.p1.y, self.p2.y)) or (
                    min(segment.p1.y, segment.p2.y) > max(self.p1.y, self.p2.y))):
                return None

            # Use the X coordinate proportions to get the displacement of first segment point over segment
            xlen = abs(segment.p2.x - segment.p1.x)
            xdist = abs(self.p1.x - segment.p1.x)
            if (xdist > xlen):
                return None
            dist = (xdist / xlen) * segment.GetLength()
            ret = segment.p1.Copy()
            ret.Move(segment.GetDirection(), dist)

            if ((ret.y < min(self.p1.y, self.p2.y)) or (ret.y > max(self.p1.y, self.p2.y))):
                return None
            else:
                return ret

        elif ((segment.p1.x - segment.p2.x) == 0):
            # Given segment is vertical

            # Now, a nice self way to get the intersection. Critics are allowed ...

            # Discard outofbounds cases
            if ((max(self.p1.x, self.p2.x) < segment.p1.x) or (min(self.p1.x, self.p2.x) > segment.p1.x)):
                return None
            if ((max(self.p1.y, self.p2.y) < min(segment.p1.y, segment.p2.y)) or (
                    min(self.p1.y, self.p2.y) > max(segment.p1.y, segment.p2.y))):
                return None

            # Use the X coordinate proportions to get the displacement of first segment point over segment
            xlen = abs(self.p2.x - self.p1.x)
            xdist = abs(self.p1.x - segment.p1.x)
            if (xdist > xlen):
                return None
            dist = (xdist / xlen) * self.GetLength()
            ret = self.p1.Copy()
            ret.Move(self.GetDirection(), dist)

            if ((ret.y < min(segment.p1.y, segment.p2.y)) or (ret.y > max(segment.p1.y, segment.p2.y))):
                return None
            else:
                return ret

        else:

            # Classical algorithm
            A1 = (self.p1.y - self.p2.y) / (self.p1.x - self.p2.x)
            A2 = (segment.p1.y - segment.p2.y) / (segment.p1.x - segment.p2.x)
            b1 = self.p1.y - (A1 * self.p1.x)
            b2 = segment.p1.y - (A2 * segment.p1.x)

            if (A1 == A2):
                return None  # Parallel segments

            ret = Point2D()
            ret.x = (b2 - b1) / (A1 - A2)
            ret.y = (A1 * ret.x) + b1

            if ((ret.x < min(self.p1.x, self.p2.x)) or (ret.x > max(self.p1.x, self.p2.x)) or (
                    ret.x < min(segment.p1.x, segment.p2.x)) or (ret.x > max(segment.p1.x, segment.p2.x))):
                return None
            else:
                if (onlycheck):
                    return True
                else:
                    return ret

        """
        d = ((self.p1.x - self.p2.x) * (segment.p1.y - segment.p2.y)) - ((self.p1.y - self.p2.y) * (segment.p1.x - segment.p2.x))
        if (d == 0):
            return None
        
        ret = Point2D()
        ret.x = (((segment.p1.x - segment.p2.x) * ((self.p1.x * self.p2.y) - (self.p1.y * self.p2.x))) - ((self.p1.x - self.p2.x) * ((segment.p1.x * segment.p2.y) - (segment.p1.y * segment.p2.x)))) / d
        ret.y = (((segment.p1.y - segment.p2.y) * ((self.p1.x * self.p2.y) - (self.p1.y * self.p2.x))) - ((self.p1.y - self.p2.y) * ((segment.p1.x * segment.p2.y) - (segment.p1.y * segment.p2.x)))) / d
       
        if ((ret.x < min(self.p1.x, self.p2.x)) or (ret.x > max(self.p1.x, self.p2.x)) or (ret.x < min(segment.p1.x, segment.p2.x)) or (ret.x > max(segment.p1.x, segment.p2.x))):
            return None
        else:
            return ret
        """

    # DEPRECATED - To check
    def ProjectSegment(self, segment):
        # Projects given segment over current one
        # WARNING: Unlike other projection methods, this one returns None if given segment doesnt fall over current one on both of their vertices. It returns the projected
        # segment if only one falls on current segment
        # WARNING (!!) : This method only runs well for segments with same direction, or different ones only when both vertices fall on current segment. See above. TODO: Fix it

        p = []
        p[0] = segment.p1.Copy()
        p[1] = segment.p2.Copy()

        # Uses the same method than point projection
        seglen = self.GetLength()
        if (seglen < 0.00000001):
            return None

        pret = []
        i = 0
        while (i < 2):
            r = (((p[i].x - self.p1.x) * (self.p2.x - self.p1.x)) + (
                        (p[i].y - self.p1.y) * (self.p2.y - self.p1.y))) / (seglen ** 2)
            if ((r < 0.00001) or (r > 1)):
                pret[i] = None
            else:
                pret[i] = Point2D(self.p1.x + r * (self.p2.x - self.p1.x), self.p1.y + r * (self.p2.y - self.p1.y))

        # Construct the segment
        if (pret[0] and pret[1]):
            return Segment2D(pret[0], pret[1])
        elif ((not pret[0]) and pret[1]):
            prj = pret[
                1].Copy()  # Note that both next cases have a mistake. If the segment direction isnt the same than current one, the
            prj.Move(-segment.GetLength(),
                     self.GetDirection())  # calculated projection point wouldnt fall on this position, so we need the projected length. We avoid
        elif (pret[0] and not pret[1]):  # to use the projected length, placing a better approach as a TODO
            prj = pret[0].Copy()
            prj.Move(segment.GetLength(), self.GetDirection())
            return Segment2D(pret[0], prj)
        else:
            return None

    def GetCloserVertex(self, point):
        # Returns the closer vertex to the given point
        dist1 = point.Distance(self.p1)
        dist2 = point.Distance(self.p2)
        if (dist1 <= dist2):
            return self.p1
        else:
            return self.p2


class Polygon2D:
    """ General 2D polygon class. Instead of store a set of sorted vertices, it stores a set of sorted segments (more memory, less cpu on some calculations)
    """

    def __init__(self):
        self.shape = []

    def Copy(self):
        ret = Polygon2D()
        for s in self.shape:
            ret.shape.append(s.Copy())
        return ret

    def GetSegmentList(self):

        ret = []
        i = 0
        while (i < len(self.shape)):
            if (i == (len(self.shape) - 1)):
                inext = 0
            else:
                inext = i + 1

            ret.append(Segment2D(self.shape[i].Copy(), self.shape[inext].Copy()))

            i += 1

        return ret

    def GetPointsList(self):

        lst = []
        for s in self.shape:
            lst.append(s.p1)

        # The polygon should be closed, so we only return the first vertex of each segment
        return lst

    def SetPointsList(self, plist):
        self.shape = []
        i = 0
        while (i < len(plist)):
            self.shape.append(Segment2D(plist[i - 1], plist[i]))
            i += 1

    def Expand(self, offset):
        # Expands the polygon by given value

        tmp = self.Copy()
        self.shape = []

        # Move all of them
        movedshape = []
        for s in tmp.shape:
            p1 = s.p1.Copy()
            p2 = s.p2.Copy()
            p1.Move(s.GetNormal(), offset)
            p2.Move(s.GetNormal(), offset)
            movedshape.append(Segment2D(p1,
                                        p2))  # Here I have a hard brain problem. If I move the segment points, why not they change in shape list? Ive tried, but
            # without any progress. For that reason Im using a second list to store the results. This is a bullshit...

        # Intersect each one with the next        
        i = 0
        while (i < len(movedshape)):
            s1 = movedshape[i]
            if (i == (len(movedshape) - 1)):
                nextt = 0
            else:
                nextt = i + 1
            s2 = movedshape[nextt]

            r1 = Ray2D(origin=s1.p1, direction=s1.GetDirection())
            r2 = Ray2D(origin=s2.p2, direction=s2.GetDirection().Invert())
            if (not r1.HitRay(r2)):
                print "ERROR: Covert Way cannot be constructed"
                i += 1
                continue

            p2 = Point2D().SetFrom3D(r1.GetHitPoint())
            movedshape[i] = Segment2D(s1.p1, p2)
            movedshape[nextt] = Segment2D(p2, s2.p2)
            self.shape.append(movedshape[i])
            if (nextt == 0):
                self.shape[0] = movedshape[0]

            i += 1

    def PurgeShortSegments(self, threshold):

        if (len(self.shape) <= 1):
            return

        tmpshape = []
        i = 0
        while (i < len(self.shape)):
            seg = self.shape[i]
            if (seg.GetLength() < threshold):
                if (i == (len(self.shape) - 1)):
                    nextseg = tmpshape[0]
                    nextseg.p1 = seg.p1
                    tmpshape[
                        0] = nextseg  # This reassignation shouldnt be necessary, but I've experienced some issues about this fact ...
                else:
                    nextseg = self.shape[i + 1]
                    nextseg.p1 = seg.p1
                    self.shape[
                        i + 1] = nextseg  # This reassignation shouldnt be necessary, but I've experienced some issues about this fact ...
            else:
                tmpshape.append(seg)

            i += 1

        self.shape = tmpshape

    def IsInside(self, p2d):
        # Returns true if given Point2D is inside the polygon
        # NOTE: This is not the classical way to calculate if a point is inside a polygon. Is just a convenient method due the context
        # Uses the classic ray-casting method: trace a ray to anywhere, if the ray intersects an odd number of polygon edges is inside

        counter = 0
        for seg in self.shape:
            ray = Ray2D(origin=p2d, direction=Vector2D(1.0, 0.0))
            # if (ray.HitSegment2(seg, inbounds = True)):
            # if (ray.CheckSegment2(seg)):
            if (ray.HitSegment3(seg)):
                counter += 1
                # ray.HitSegment3(seg)

        if ((counter % 2) == 0):
            return False
        else:
            return True

    def Intersect(self, poly):
        # Returns True if both polygons intersects.
        # The intersection point cannot be returned because one polygon could be placed completely inside the other

        # Check edge intersections
        for seg in self.shape:
            for seg2 in poly.shape:
                if (seg.Intersect(segment=seg2, margin=0, onlycheck=True)):
                    return True

        # Check vertices inside condition
        for seg in self.shape:
            if poly.IsInside(seg.p1):
                return True

        for seg in poly.shape:
            if self.IsInside(seg.p1):
                return True

        return False

    def SwitchOrientation(self):
        # Switchs the polygon vertices orientation (clockwise or inverse)

        index = -1
        tmplist = []

        while (index >= -len(self.shape)):
            seg = self.shape[index]
            tmplist.append(Segment2D(seg.p2, seg.p1))
            index -= 1

        self.shape = tmplist

    def IsCloserToVertex(self, point, margin=10.0):
        # Returns None if given point isnt closer to any polygon vertex. Otherwise, returns the closer vertex

        i = 0
        while (i < len(self.shape)):
            if (point.Distance(self.shape[i].p1) < margin):
                return self.shape[i].p1.Copy()
            i += 1

        return None

    def GetCloserSegment(self, point, margin=10.0):
        # Returns the closer segment to given point

        seg = None
        dmin = -1
        for s in self.shape:
            prj = s.ProjectPoint(point=point, forceprojection=True)
            if (prj != None):
                dist = prj.Distance(point)
                if (dmin == -1):
                    seg = s
                    dmin = dist
                else:
                    if (dmin > dist):
                        dmin = dist
                        seg = s

        if (dmin < margin):
            return seg
        else:
            return None

    def GetBoundingBox(self):

        ret = BoundingQuad()
        for s in self.shape:
            ret.InsertPoint(s.p1)

        return ret


class Vector3D():
    def __init__(self, x=0, y=0, z=0):
        self.val = [x, y, z]

    def Copy(self):
        v = Vector3D(self.val[0], self.val[1], self.val[2])
        return v

    def SetFrom2D(self, v2d):
        self.val[0] = v2d.val[0]
        self.val[1] = v2d.val[1]
        self.val[2] = 0

        return self

    def Invert(self):
        self.val[0] = -self.val[0]
        self.val[1] = -self.val[1]
        self.val[2] = -self.val[2]

        return self

    def IsNull(self):
        if ((self.val[0] == 0) and (self.val[1] == 0) and (self.val[2] == 0)):
            return True
        else:
            return False

    def CreateFrom2Points(self, p1, p2, normalize=True):
        self.val[0] = p2.x - p1.x
        self.val[1] = p2.y - p1.y
        self.val[2] = p2.z - p1.z
        if (normalize):
            self.Normalize()

        return self

    def Module(self):
        return math.sqrt((self.val[0] ** 2) + (self.val[1] ** 2) + (self.val[2] ** 2))

    def Normalize(self):
        l = self.Module()
        if (l == 0):
            self.val[0] = 0
            self.val[1] = 0
            self.val[2] = 0
        else:
            self.val[0] /= l
            self.val[1] /= l
            self.val[2] /= l

    def DotProd(self, v):
        return (self.val[0] * v.val[0]) + (self.val[1] * v.val[1]) + (self.val[2] * v.val[2])

    def CrossProd(self, v):

        cp = Vector3D()

        cp.val[0] = (self.val[1] * v.val[2]) - (v.val[1] * self.val[2])
        cp.val[1] = (self.val[2] * v.val[0]) - (v.val[2] * self.val[0])
        cp.val[2] = (self.val[0] * v.val[2]) - (v.val[0] * self.val[1])

        return cp

    def AngleBetween(self, v):
        # Returns the angle between current and given vector   
        dotprod = self.DotProd(v)
        if (dotprod > 1):
            dotprod = 1
        elif (dotprod < -1):
            dotprod = -1
        rad = math.acos(dotprod)
        return math.degrees(rad)


class Sphere:
    """ Sphere class. Used mainly to get sampling distributions
    """

    def __init__(self, radius=1.0, position=Point3D()):
        self.__radius = radius
        self.__position = position

    def GetRndPointNormal(self):
        # Get a random vector from sphere's center
        # Rejection method
        # seed()

        v = Vector3D()

        length = 999.9
        while ((length > 1.0) and (length != 0)):
            i = 0
            while (i < 3):
                v.val[i] = (2.0 * random()) - 1.0  # coordinates distributed in [-1..1]
                i += 1
            length = v.Module()
        v.Normalize()

        # Return the point over sphere
        return Point3D((v.val[0] + self.__position.x) * self.__radius, (v.val[1] + self.__position.y) * self.__radius,
                       (v.val[2] + self.__position.z) * self.__radius)

    def GetRndPoint(self, ):
        # Sampling on a sphere by trigonometric method (faster than rejection one)
        # seed()

        phi = 2.0 * math.pi * random()
        theta = math.acos(1.0 - (2.0 * random()))

        ret = Point3D()
        ret.x = (math.sin(theta) * math.cos(phi) * self.__radius) + self.__position.x
        ret.y = (math.sin(theta) * math.sin(phi) * self.__radius) + self.__position.y
        ret.z = (math.cos(theta) * self.__radius) + self.__position.z

        return ret

    def GetRayCosine(self, direction):
        # Returns a sampled vector in basis on a cosine distribution from current sphere's center and given direction
        # Note that increasing the radius we get a more stretch distribution

        # Get the point over sphere using given direction
        p = self.__position.Copy()
        p.Move(direction, self.__radius)

        # Consider p as the center of a new sphere of radius 1
        # Sample a point over this sphere
        sph2 = Sphere(position=p, radius=1.0)
        p2 = sph2.GetRndPoint()

        # The vector is constructed from central point to new point over second sphere
        v2 = Vector3D().CreateFrom2Points(self.__position, p2)

        return v2


class Ray2D:
    """ Simple ray class. It works on 2D space.
    
    Atributes:
        from: Origin point
        direction: Ray Direction
        hitPoint: Hit point 
    """

    def __init__(self, origin=Point2D(), direction=Vector2D()):
        self.__from = origin
        self.__direction = direction
        self.__hitPoint = Point3D()

    def SetFrom3D(self, ray3d):
        self.__from = Point2D().SetFrom3D(ray3d.GetOrigin())
        self.__direction = Vector2D().SetFrom3D(ray3d.GetDirection())
        self.__hitPoint = Point2D().SetFrom3D(ray3d.GetHitPoint())
        return self

    def Reset(self):
        self.__hitPoint = Point3D()

    def GetHitPoint(self):
        return self.__hitPoint

    def GetLength(self):
        # Returns the distance from origin to hit point
        return self.__from.Distance(self.__hitPoint)

    # Try to hit current ray onto given segment. If inbounds is false, the given segment is converted to a ray. Otherwise, only returns
    # true if the hitpoint falls on the segment bounds
    # NOTE: I'm not sure about this function works well .... try HitSegment2
    def HitSegment(self, seg, inbounds=False):

        ray = Ray2D(origin=seg.p1, direction=seg.GetDirection())

        if (not inbounds):
            return self.HitRay(ray)
        else:
            if (self.HitRay(ray)):
                # At this point the intersection point is on the segment-vector. A simple check on the segment boundaries should
                # be enough to know if the intersection point is on the segment
                bound = BoundingQuad()
                bound.InsertPoint(seg.p1)
                bound.InsertPoint(seg.p2)
                if (seg.p1.Distance(self.__hitPoint) <= seg.GetLength()):  # and bound.IsInside(self.__hitPoint)):
                    return True
                else:
                    return False
            else:
                return False

                # Some bugs. Try HitSegment3

    def HitSegment2(self, seg, inbounds=False):

        ray = Ray2D(origin=seg.p1, direction=seg.GetDirection())

        if (not inbounds):
            return self.HitRay(ray)
        else:
            if (self.HitRay(ray)):
                # At this point the intersection point is on the segment-vector. A simple check on the segment boundaries should
                # be enough to know if the intersection point is on the segment
                bound = BoundingQuad()
                bound.InsertPoint(seg.p1)
                bound.InsertPoint(seg.p2)
                if (bound.IsInside(self.__hitPoint)):
                    # if (seg.p1.Distance(self.__hitPoint) <= seg.GetLength()):      # and bound.IsInside(self.__hitPoint)):
                    if self.CheckSegment2(seg):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

    def CheckSegment2(self, segment):
        # Uses a different intersection approach. Just check if ray direction vector is between the vectors from ray origin to segment vertices
        # BE AWARE: This function only checks if there is any intersection, but doesnt calculates the intersection point

        v1 = Vector2D().CreateFrom2Points(self.__from, segment.p1)
        v2 = Vector2D().CreateFrom2Points(self.__from, segment.p2)

        cp1 = v1.CrossProd(self.__direction)
        cp2 = self.__direction.CrossProd(v2)

        if ((cp1 * cp2) >= 0):
            return True
        else:
            return False

    def HitSegment3(self, segment):

        # Another classical ray-segment intersection algorithm
        # Be aware. The vectors cannot be normalized, so we are not working in a normalized/tangent space
        segvec = Vector2D(segment.p2.x - segment.p1.x, segment.p2.y - segment.p1.y)
        segperp = Vector2D(segvec.val[1], -segvec.val[0])
        perpdot = self.__direction.DotProd(segperp)

        if (perpdot == 0):
            return False

        if (math.fabs(perpdot) <= 0.00001):
            # parallel case
            return False
        else:

            d = Vector2D().CreateFrom2Points(self.__from, segment.p1, normalize=False)
            t = segperp.DotProd(d) / perpdot
            svec = Vector2D(self.__direction.val[1], -self.__direction.val[0])
            s = svec.DotProd(d) / perpdot

            if ((t >= 0.0) and (s >= 0.0) and (s <= 1.0)):

                self.__hitPoint = self.__from.Copy()
                self.__hitPoint.Move(self.__direction, t)

                return True
            else:
                return False

    def HitBoundingQuad(self, bquad):

        seglst = bquad.GetSegments()
        for seg in seglst:
            if (self.HitSegment(seg, inbounds=True)):
                return True
        return False

    def HitRay(self, r2):
        # Calculate the intersection point between current ray and given one in 2D
        # Returns true if there is an intersection. The intersected point (in 2D) can be taken from self.__hitPoint

        self.__hitPoint = Point2D()

        # The most efficient way to calculate it (note that this isnt the classic line-to-line intersection algorithm, so rays are involved)

        # Special cases
        selfnear0 = ((self.__direction.val[0] >= -0.00001) and (self.__direction.val[0] <= 0.00001))
        r2near0 = ((r2.__direction.val[0] >= -0.00001) and (r2.__direction.val[0] <= 0.00001))
        """
        if (selfnear0 and r2near0):
            # Parallel rays
            return False
        elif (selfnear0):
            # Current ray is parallel to X axis
            # Solve the linear equation mathing the y value of intersection point
            self.__hitPoint.y = self.__from.y;
            t = (self.__hitPoint.y - r2.__from.y) / r2.__direction.val[1]
            self.__hitPoint.x = r2.__from.x + (t * r2.__direction.val[0])
            
            
            
        elif (r2near0):
            
        else:
        """

        # TODO: Finish the special cases

        if (selfnear0):
            selfdirx = 0.000001
        else:
            selfdirx = self.__direction.val[0]

        if (r2near0):
            r2dirx = 0.000001
        else:
            r2dirx = r2.__direction.val[0]

        # Normal case

        grad1 = self.__direction.val[1] / selfdirx
        grad2 = r2.__direction.val[1] / r2dirx
        ray1c = self.__from.y - (self.__from.x * grad1)
        ray2c = r2.__from.y - (r2.__from.x * grad2)

        if (grad1 == grad2):
            # Parallel lines
            return False

        self.__hitPoint.x = (ray2c - ray1c) / (grad1 - grad2)
        self.__hitPoint.y = (grad1 * self.__hitPoint.x) + ray1c

        return True

    def HitCircle(self, circle):

        # Ray-circle intersection

        # From the ray equation, replace the circle equation x^2+y^2-R^2, giving a 2nd order equation to solve over the ray displacement vector value
        # Remember to normalize the circle and ray to the origin

        pos = self.__from.Copy()
        pos.x -= circle.GetCenter().x
        pos.y -= circle.GetCenter().y

        A = math.pow(self.__direction.val[0], 2) + math.pow(self.__direction.val[1], 2)
        B = 2.0 * ((pos.x * self.__direction.val[0]) + (pos.y * self.__direction.val[1]))
        C = math.pow(pos.x, 2) + math.pow(pos.y, 2) - math.pow(circle.GetRadius(), 2)
        # C = math.pow(pos.x, 2) + math.pow(pos.y, 2) - 1

        root = math.pow(B, 2) - (4.0 * A * C)
        if (root <= 0):
            return False
        else:

            t1 = (-B + math.sqrt(root)) / (2.0 * A)
            t2 = (-B - math.sqrt(root)) / (2.0 * A)

            t = min(t1, t2)

            self.__hitPoint = self.__from.Copy()
            self.__hitPoint.Move(vector=self.__direction, offset=t)

            return True


class Ray:
    """ Simple ray class. It works on 3D space.
    
    Atributes:
        from: Origin point
        direction: Ray Direction
        energy: Scalar value that represents the energy, attack factor, ...
        hitPoint: Hit point 
    """

    def __init__(self, origin=Point3D(), direction=Vector3D(), energy=0.0):
        self.__from = origin
        self.__direction = direction
        self.__energy = energy
        self.__hitPoint = Point3D()

    def Reset(self):
        self.__hitPoint = Point3D()

    def GetOrigin(self):
        return self.__from

    def GetHitPoint(self):
        return self.__hitPoint

    def SetHitPoint(self, p):
        self.__hitPoint = p

    def GetLength(self):
        # Returns the distance from origin to hit point
        return self.__from.Distance(self.__hitPoint)

    def GetDirection(self):
        return self.__direction

    def HitRectangle(self, rectangle, bounds, normal):
        # Calculates the intersection point of current ray on given rectangle
        # Returns true if hit succeed
        # Given rectangle is a list with four 3D points that define the rectangle, and the rectangle normal vector
        # Given bounds parameter the rectangle bounding box
        # The normal vector is used to discard back hits

        ret = False

        dirx = self.__direction.val[0]
        diry = self.__direction.val[1]
        dirz = self.__direction.val[2]

        planex = normal.val[0]
        planey = normal.val[1]
        planez = normal.val[2]

        # First checks if plane orientation is in front of ray
        # if (normal.DotProd(self.__direction) > 0):
        tt = (planex * dirx) + (planey * diry) + (planez * dirz)
        if (tt > 0):
            return False

        # Get the plane equation
        anypoint = rectangle[0]
        planeq = -(planex * anypoint.x) - (planey * anypoint.y) - (planez * anypoint.z)

        # We can use the t parameter of parametric ray form R(t) = R0 + Rd*t to get the point where t = -(A*x0 + B*y0 + C*z0 + D) / (A*xd + B*yd + C*zd)    
        if (tt == 0):
            return False
        t = -((planex * self.__from.x) + (planey * self.__from.y) + (planez * self.__from.z) + planeq) / tt

        if (t >= 0):
            # Get the intersection point
            prj = Point3D(self.__from.x + (dirx * t), self.__from.y + (diry * t), self.__from.z + (dirz * t))

            # Check if ray lies on rectangle
            if (bounds.IsInside(prj)):
                self.__hitPoint = prj
                ret = True

        return ret

    def GetCosEnergy(self, normal):
        # Returns the energy weighted by angle of incidence and given normal.
        # Note that the incidence vector must be inverted to be compared with the normal vector
        v = Vector3D().CreateFrom2Points(self.__hitPoint, self.__from)
        cos = v.DotProd(normal)
        return self.__energy * cos

    def HitCylinder(self, center, radius, height):
        # ray-cylinder intersection test. Caps are not considered

        px = self.__from.x - center.x
        py = self.__from.y - center.y
        dx = self.__direction.val[0]
        dy = self.__direction.val[1]

        # Replace the cylinder equation x^2 + y^2 = r^2 by ray equation p + t * d and solve t
        a = -(px * dx + py * dy)
        b1_a = (px * dx + py * dy) ** 2
        b1_b = (dx ** 2) + (dy ** 2)
        b1_c = (px ** 2) + (py ** 2) - (radius ** 2)
        b1 = b1_a - (b1_b * b1_c)
        if (b1 < 0):
            return False
        b = math.sqrt(b1)
        c = (dx ** 2) + (dy ** 2)

        if (c == 0):
            return False

        t1 = (a + b) / c
        t2 = (a - b) / c

        if ((t1 <= t2) and (t1 >= 0)):
            t = t1
        elif (t2 >= 0):
            t = t2
        else:
            return False

        prj = self.__from.Copy()
        prj.Move(self.__direction, t)

        if ((prj.z < 0) or (prj.z > height)):
            return False
        else:
            self.__hitPoint = prj
            return True

    def HitBox(self, box):

        tx1 = (box.min.x - self.__from.x) / self.__direction.val[0]
        tx2 = (box.max.x - self.__from.x) / self.__direction.val[0]
        ty1 = (box.min.y - self.__from.y) / self.__direction.val[1]
        ty2 = (box.max.y - self.__from.y) / self.__direction.val[1]
        tz1 = (box.min.z - self.__from.z) / self.__direction.val[2]
        tz2 = (box.max.z - self.__from.z) / self.__direction.val[2]

        tmin = max(max(min(tx1, tx2), min(ty1, ty2)), min(tz1, tz2))
        tmax = min(min(max(tx1, tx2), max(ty1, ty2)), max(tz1, tz2))

        if (tmin > tmax):
            return False
        elif (tmax < 0):
            return False
        else:
            t = tmin

            self.__hitPoint = self.__from.Copy()
            self.__hitPoint.Move(self.__direction, t)

            return True


class Bounding:
    """ Simple cube bounding used for army components
    """

    def __init__(self, length, width, height=0.0):
        self.length = length
        self.width = width
        self.height = height

    def GetVolume(self):
        return self.length * self.width * self.height


class BoundingQuad:
    """ Bounding quad with min and maximum 2D points
        WARNING: This class is now used as Bounding Box 2D, not quad (could be a rectangle). The name is retained (I don't like refactoring the code)
    """

    def __init__(self, minPoint=Point2D(), maxPoint=Point2D()):
        self.minPoint = minPoint
        self.maxPoint = maxPoint
        self.count = 0


    def get_min(self):
        return self.minPoint

    def get_max(self):
        return self.maxPoint

    def FromCenterSize(self, center, size):
        self.minPoint = Point2D(center.x - (size / 2.0), center.y - (size / 2.0))
        self.maxPoint = Point2D(center.x + (size / 2.0), center.y + (size / 2.0))
        return self

    def InsertPoint(self, point):
        if (self.count == 0):
            self.maxPoint = point.Copy()
            self.minPoint = point.Copy()
        else:
            if (point.x < self.minPoint.x):
                self.minPoint.x = point.x
            if (point.y < self.minPoint.y):
                self.minPoint.y = point.y
            if (point.x > self.maxPoint.x):
                self.maxPoint.x = point.x
            if (point.y > self.maxPoint.y):
                self.maxPoint.y = point.y

        self.count += 1

    def InsertBounding(self, bound):
        self.InsertPoint(bound.minPoint)
        self.InsertPoint(bound.maxPoint)

    def GetLength(self):
        return math.fabs(self.maxPoint.x - self.minPoint.x)

    def GetWidth(self):
        return math.fabs(self.maxPoint.y - self.minPoint.y)

    def GetCenter(self):
        p = Point2D()
        p.x = self.minPoint.x + ((self.maxPoint.x - self.minPoint.x) / 2.0)
        p.y = self.minPoint.y + ((self.maxPoint.y - self.minPoint.y) / 2.0)
        return p

    def GetSegments(self):

        ret = [Segment2D(self.minPoint, Point2D(self.maxPoint.x, self.minPoint.y)),
               Segment2D(Point2D(self.maxPoint.x, self.minPoint.y), self.maxPoint),
               Segment2D(self.maxPoint, Point2D(self.minPoint.x, self.maxPoint.y)),
               Segment2D(Point2D(self.minPoint.x, self.maxPoint.y), self.minPoint)]

        return ret

    def IsInside(self, p):
        return ((p.x >= self.minPoint.x) and (p.x <= self.maxPoint.x) and (p.y >= self.minPoint.y) and (
                    p.y <= self.maxPoint.y))

    def IntersectSegment(self, segment):

        if (self.IsInside(segment.p1) or self.IsInside(segment.p2)):
            return True
        else:
            return False  # TODO: Check the intersection of segment edge with both segment vertices outside the bounding

    def GetVertices(self):
        # Return a list with the four bounding  vertices

        ret = [self.minPoint.Copy(), Point2D(self.maxPoint.x, self.minPoint.y), self.maxPoint.Copy(),
               Point2D(self.minPoint.x, self.maxPoint.y)]

        return ret

    def Expand(self, margin):

        self.minPoint.x -= margin
        self.minPoint.y -= margin
        self.maxPoint.x += margin
        self.maxPoint.y += margin

    def GetBoundingCircle(self):

        # The circle diameter should be the longer distance between two points
        seg = Segment2D(self.minPoint, self.maxPoint)

        return Circle(center=seg.GetMidPoint(), radius=seg.GetLength() / 2.0)


class BoundingBox:
    """ 3D bounding class
    """

    def __init__(self, minP=Point3D(), maxP=Point3D()):
        self.min = minP
        self.max = maxP
        self.count = 0

    def InsertPoint(self, point):
        # Updates the bounding if point falls off current bounding box
        if (self.count == 0):
            self.min = point.Copy()
            self.max = point.Copy()
        else:

            if (point.x < self.min.x):
                self.min.x = point.x
            if (point.y < self.min.y):
                self.min.y = point.y
            if (point.z < self.min.z):
                self.min.z = point.z
            if (point.x > self.max.x):
                self.max.x = point.x
            if (point.y > self.max.y):
                self.max.y = point.y
            if (point.z > self.max.z):
                self.max.z = point.z

        self.count += 1

    def IsInside(self, point):
        # Returns True if given point is inside current bounding
        if ((point.x >= self.min.x) and (point.y >= self.min.y) and (point.z >= self.min.z) and (
                point.x <= self.max.x) and (point.y <= self.max.y) and (point.z <= self.max.z)):
            return True
        else:
            return False

    def GetVolume(self):
        l = math.fabs(self.max.x - self.min.x)
        w = math.fabs(self.max.y - self.min.y)
        h = math.fabs(self.max.z - self.min.z)

        return l * w * h


class TerrainBounding:
    """ Simple 2D terrain bounding defined by a bottom and top points
    """

    def __init__(self, bot, top):
        self.bottom = bot
        self.top = top

    def GetLength(self):
        return self.top.x - self.bottom.x

    def GetWidth(self):
        return self.top.y - self.bottom.y

    def Crop(self, bounding):
        # Crops current bounding with given one
        if (self.bottom.x < bounding.bottom.x):
            self.bottom.x = bounding.bottom.x
        if (self.bottom.y < bounding.bottom.y):
            self.bottom.y = bounding.bottom.y
        if (self.top.x > bounding.top.x):
            self.top.x = bounding.top.x
        if (self.top.y > bounding.top.y):
            self.top.y = bounding.top.y


class Slope:
    """ Represents the ramped exterior curtain wall
    
    Attributes:
        angle: Slope angle from ground. (degrees)
        height: Slope height (meters)
    """

    def __init__(self):
        self.angle = 45.0
        self.height = 2.0


class Viewport:
    """ Viewport class to transform coordinates between a view and window coordinate system. It works with the TKinter canvas coordinate system
         
    Attributes:
        view: Bounding with view size (Bounding class)
        world: Bounding with world size (Bounding class)
        offset: Viewport minimum bounding position (Point2D class)
    """

    def __init__(self, viewSize, worldSize, offset=Point2D()):
        self.__view = {"length": viewSize.length, "height": viewSize.width}
        self.__world = {"length": worldSize.length, "height": worldSize.width}
        self.__offset = offset

    def SetOffset(self, offset):
        self.__offset = offset

    def GetOffset(self):
        return self.__offset

    def W2V(self, p1):
        # Transforms a Point2D object in view coordinates to window coordinates

        pv = Point2D()

        # Viewport scale by axis
        factorX = self.__view["length"] / self.__world["length"]
        factorY = self.__view["height"] / self.__world["height"]
        if (factorX < factorY):
            factor = factorY
        else:
            factor = factorX

        # Scale factor to fit all board
        if (self.__world["length"] >= self.__world["height"]):
            scale = self.__world["height"] / self.__world["length"]
        else:
            scale = self.__world["length"] / self.__world["height"]

        pv.x = (self.__offset.x + p1.x) * factor * scale
        pv.y = (self.__offset.y + p1.y) * factor * scale

        return pv

    def W2V_1f(self, x):
        # Transforms a float size value in view coordinates to window coordinates

        # Let's do a simple and stupid trick
        p = self.W2V(Point2D(x, x))

        return p.x

    def Zoom(self, z):

        oldl = self.__view["length"]
        oldh = self.__view["height"]
        self.__view["length"] *= z
        self.__view["height"] *= z

        self.__offset.x = (self.__view["length"] - oldl) / 2.0
        self.__offset.y = (self.__view["height"] - oldh) / 2.0


class ClusteringKMeans:
    """ Clustering class. Uses the k-means method and euclidean distance for 2D and 3D list of points.
        Some personal considerations on the algorithm have been taken, such as the initial means (N points from inital points list are taken as initial means)
    
    Attributes:
    
        points: List of points to clusterize
        initialNMeans : Number of initial means
        maxIterations: Maximum number of clustering iterations
    """

    def __init__(self, points, initialMeans, maxiterations=100):
        self.__points = points
        """
        if (initialmeans < 2):
            self.__initialNMeans = 2
            Message.Log('Initial number of means has to be greater than 2', Message.VERBOSE_WARNING)
        elif (initialmeans >= len(self.__points)):
            self.__initialNMeans = len(self.__points)
            Message.Log('Initial number of means cannot be greater than point list size', Message.VERBOSE_WARNING)
        else:
            self.__initialNMeans = initialmeans
        """

        if (len(points) < initialMeans):
            self.__initialNMeans = 1
        else:
            self.__initialNMeans = initialMeans

        self.__maxIterations = maxiterations
        self.__clusters = []

    def execute(self):

        if (len(self.__points) == 0):
            return

        # Take the N initial means from points list
        del self.__clusters[0:len(self.__clusters)]
        i = 0
        while (i < self.__initialNMeans):
            self.__clusters.append({"mean": self.__points[i], "points": []})
            i += 1

        # Assign each point to nearest cluster
        point2cluster = []  # Relates the point with cluster. Has as many elements as points, and each index is the related cluster index
        nclusters = self.__initialNMeans
        for p in self.__points:
            dmin = -1
            imin = -1
            i = 0
            while (i < nclusters):
                d = p.Distance(self.__clusters[i]["mean"]) ** 2
                if ((i == 0) or (d < dmin)):
                    dmin = d
                    imin = i
                i += 1

            self.__clusters[imin]["points"].append(p)
            point2cluster.append(imin)

        stop = False
        loops = 0
        while ((not stop) and (loops < self.__maxIterations)):

            # Recalculate the clusters means
            for c in self.__clusters:
                size = len(c["points"])
                if (size > 0):
                    i = 1
                    accum = c["points"][0]
                    while (i < size):
                        accum.Sum(c["points"][i])
                        i += 1
                    c["mean"] = accum.Div(size)
                    del c["points"][0:len(c["points"])]

            # Reassign points to new cluster means
            stop = True
            j = 0
            while (j < len(self.__points)):
                p = self.__points[j]
                dmin = -1
                imin = -1
                i = 0
                while (i < nclusters):
                    d = p.Distance(self.__clusters[i]["mean"]) ** 2
                    if ((i == 0) or (d < dmin)):
                        dmin = d
                        imin = i
                    i += 1

                self.__clusters[imin]["points"].append(p)
                if (point2cluster[j] != imin):
                    stop = False
                point2cluster[j] = imin

                j += 1

            loops += 1

    def GetLargestCluster(self):
        # Return the largest cluster mean

        if (len(self.__clusters) == 0):
            return None

        sizemax = -1
        meanmax = None
        for c in self.__clusters:
            size = len(c["points"])
            if (size > sizemax):
                sizemax = size
                meanmax = c["mean"]

        return meanmax


class ConvexHull():
    """ Calculates the convex hull of a given set of points. Uses the classic gift wrapping algorithm
        Given ponts have [x,y] format. They AREN'T Point2D (use SetPoint2DList method for Point2D data)
    """

    TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)

    def __init__(self, points):
        self.points = points
        self.hull = []

    def SetPoint2DList(self, lst):

        self.points = []
        for p in lst:
            self.points.append([p.x, p.y])

    def GetNPoints(self):
        return len(self.hull)

    def Get2DPointHull(self):
        # Returns the hull polyline in a Point2D polyline format

        lst = []
        for h in self.hull:
            lst.append(Point2D(h[0], h[1]))

        return lst

    def GetSegmentList(self):

        seglst = []
        i = 0
        while (i < len(self.hull)):

            if (i >= (len(self.hull) - 1)):
                seg = Segment2D(Point2D(self.hull[i][0], self.hull[i][1]), Point2D(self.hull[0][0], self.hull[0][1]))
            else:
                seg = Segment2D(Point2D(self.hull[i][0], self.hull[i][1]),
                                Point2D(self.hull[i + 1][0], self.hull[i + 1][1]))

            seglst.append(seg)
            i += 1

        return seglst

    def GetPolygon2D(self):

        poly = Polygon2D()
        poly.shape = self.GetSegmentList()

        return poly

    def Calculate(self):

        self.hull = []

        # Get the minimum left point
        self.hull.append(min(self.points))

        for p in self.hull:
            q = self.__NextHullPoint(p)
            if q != self.hull[0]:
                self.hull.append(q)
        return self.hull

    def __NextHullPoint(self, p):

        q = p
        for r in self.points:
            t = self.__Turn(p, q, r)

            d1 = self.__Distance(p, r)
            d2 = self.__Distance(p, q)

            if t == self.TURN_RIGHT or t == self.TURN_NONE and d1 > d2:
                q = r

        return q

    # Returns -1, 0, 1 if p,q,r forms a right, straight, or left turn."""
    def __Turn(self, p, q, r):
        return cmp((q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1]), 0)

    def __Distance(self, p, q):
        dx, dy = q[0] - p[0], q[1] - p[1]
        return dx * dx + dy * dy

    def SetMargin(self, margin):
        # Sets the given margin offset to hull polygon

        # Calculate the bounding box
        bbox = BoundingQuad()
        for p in self.hull:
            bbox.InsertPoint(Point2D(p[0], p[1]))

        # Expand hull vertices from bounding box center
        # TODO: Improve with a more accurate method
        center = bbox.GetCenter()

        i = 0
        while (i < len(self.hull)):
            p = self.hull[i]
            p2d = Point2D(p[0], p[1])
            v = Vector2D().CreateFrom2Points(center, p2d)
            p2d.Move(v, margin)
            self.hull[i] = [p2d.x, p2d.y]

            i += 1

    def IsInside(self, p2d):
        # Returns true if given Point2D is inside the convex hull

        lastp = Point2D(self.hull[0][0], self.hull[0][1])
        i = 1
        while (i < (len(self.hull))):
            currp = Point2D(self.hull[i][0], self.hull[i][1])
            v = Vector2D().CreateFrom2Points(lastp, currp, False)
            vv = Vector2D().CreateFrom2Points(lastp, p2d, False)
            if (v.Det(vv) < -0.0001):
                return False

            lastp = currp
            i += 1

        currp = Point2D(self.hull[0][0], self.hull[0][1])
        v = Vector2D().CreateFrom2Points(lastp, currp, False)
        vv = Vector2D().CreateFrom2Points(lastp, p2d, False)
        if (v.Det(vv) < -0.0001):
            return False
        else:
            return True

    def PurgeSmallSegments(self, minlen):
        # Remove the convex hull segments smaller than given length
        # The adjacent vertices will be extended to their intersection (avoiding the creation of a convex hull with outer points

        # Work with segments (making it easy)
        seglist = self.GetSegmentList()
        tmplist = []
        i = 0
        while (i < len(seglist)):
            seg = seglist[i]
            if (seg.GetLength() < minlen):

                seglast = seglist[i - 1]
                if ((i + 1) >= len(seglist)):
                    segnext = seglist[0]
                else:
                    segnext = seglist[i + 1]

                ray1 = Ray2D(origin=seglast.p1, direction=seglast.GetDirection())
                ray2 = Ray2D(origin=segnext.p2, direction=segnext.GetDirection().Invert())
                if (not ray1.HitRay(ray2)):
                    print "ERROR purgin the convex hull"
                    continue

                seglast.p2 = ray1.GetHitPoint()
                segnext.p1 = ray1.GetHitPoint()

            else:
                tmplist.append(seg)

            i += 1

        # Translate the final segment list to convex hull points
        self.hull = []
        for s in tmplist:
            self.hull.append([s.p1.x, s.p1.y])

    def SplitLongSegments(self, maxlen):
        # Splits all segments longer than given maximum length
        # WARNING: This method can generate small segments. So it should be called before the PurgeSmallSegments method (if you need to purgue the small ones)

        if (maxlen <= 0):
            return

        seglist = self.GetSegmentList()
        tmplist = []
        i = 0
        while (i < len(seglist)):
            seg = seglist[i]
            slength = seg.GetLength()
            sdir = seg.GetDirection()
            if (slength > maxlen):
                splits = math.floor(slength / maxlen)

                # Divide the segment into splits
                plast = seg.p1.Copy()
                pnext = seg.p1.Copy()
                j = 0
                while (j < splits):
                    pnext.Move(sdir, maxlen)
                    tmplist.append(Segment2D(plast, pnext))
                    plast = pnext.Copy()
                    j += 1

                # Get final segment part (shorter)
                pnext = seg.p2.Copy()
                tmplist.append(Segment2D(plast, pnext))

                # Do not store the splitted segment
            else:
                tmplist.append(seg)

            i += 1

        # Translate the final segment list to convex hull points
        self.hull = []
        for s in tmplist:
            self.hull.append([s.p1.x, s.p1.y])


class Circle:

    def __init__(self, center, radius):
        self.__center = center
        self.__radius = radius

    def GetCenter(self):
        return self.__center

    def GetRadius(self):
        return self.__radius

    def SetRadius(self, r):
        self.__radius = r

    def IntersectionCircle(self, circle):
        # Return the two intersection points between current circle and given one (or None if there arent)

        ret = [None, None]

        # Check that both circles intersect
        dist = self.__center.Distance(circle.__center)
        if ((dist > (self.__radius + circle.__radius)) or  # Both circles are too far from each other
                (dist < math.fabs(self.__radius - circle.__radius)) or  # One circle is inside the other
                ((dist == 0) and (self.__radius == circle.__radius))):  # Same circles
            return ret

        # Find the perpendicular segment to the segment between circles centers and to the intersection points
        # Do some trigonometry to get 'a' as the distance from current circle center to perpendicular segment intersection on segment between circles centers (yeah, too much
        # hard to explain without a draw). Just check the classic algorithm to get circle-circle intersection
        a = ((self.__radius ** 2) - (circle.__radius ** 2) + (dist ** 2)) / (2.0 * dist)
        h = math.sqrt(self.__radius ** 2 - a ** 2)

        vec1 = Vector2D().CreateFrom2Points(circle.__center, self.__center)
        vec2 = vec1.GetPerpendicular()

        ret[0] = self.__center.Copy()
        ret[0].Move(vec1, a)
        ret[0].Move(vec2, h)

        ret[1] = ret[0].Copy()
        ret[1].Move(vec2, -(h * 2.0))

        """
        # Get the intersection point of h segment
        hx = self.__center.x + ((a * (circle.__center.x - self.__center.x)) / dist)
        hy = self.__center.y + ((a * (circle.__center.y - self.__center.y)) / dist)
        
        # Now we can get both intersection points moving along this segment
        ret[0] = Point2D()
        ret[0].x = (hx + (h * (circle.__center.y - self.__center.y))) / dist
        ret[0].y = (hy - (h * (circle.__center.x - self.__center.x))) / dist
        ret[1] = Point2D()
        ret[1].x = (hx - (h * (circle.__center.y - self.__center.y))) / dist
        ret[1].y = (hy + (h * (circle.__center.x - self.__center.x))) / dist
        """

        return ret

    def TangentPointsFromPoint(self, point):
        # Return the circle tangent points from the given point

        # We have the distance from center to point. In addition, we know that circle tangent points are 90-degree to the circle center. So we can get the distance between
        # point and tangent points by simple trigonometry

        dist = self.__center.Distance(point)
        tdist = math.hypot(dist, self.__radius)

        # Now, if we have a cercle of center the given point and radius the calculated distance, we can calculate the circle-circle intersections
        circle = Circle(center=point, radius=tdist)
        tgntpnts = self.IntersectionCircle(circle)

        return tgntpnts

    def GetPolygon(self, sides):
        # Return the circle shape in polygon form with given number of sides

        ret = []
        if (sides <= 0):
            return ret

        angle = 360.0 / sides

        plast = self.__center.Copy()
        plast.MoveAngle(self.__radius, 0)

        i = 1
        while (i <= sides):
            p = self.__center.Copy()
            p.MoveAngle(angle * i, self.__radius)
            ret.append(Segment2D(plast.Copy(), p))
            plast = p
            i += 1

        return ret


class GPCWrapper:
    """
    GPC (the 2D shape clipping library) wrapper on Polygon port (see http://www.j-raedler.de/projects/polygon/)

    Instead of using GPC polygon objects along the project, all data will be specified as point lists and transformed internally.
    This is slow, but most effective, so it helps on a possible change of clipping library
    TODO: Create an interface to be derived by this class, allowing other derived clipping libraries
    """

    def __init__(self, tolerance=0.001):
        Polygon.setTolerance(tolerance)

    # Return a polygon contourn from the given Point2D object list
    def GetContour(self, point2dlist):
        lst = []
        for p in point2dlist:
            lst.append([p.x, p.y])
        return lst

    # Returns a Point2D list from a Polygon object
    def GetPoint2DList(self, poly):
        lst = []
        for contour in poly:
            for vertex in contour:
                lst.append(Point2D(vertex[0], vertex[1]))
        return lst

    # Performs the difference operation between 2 Point2D object lists. Scale values are applied to each list to expand or reduce the polygons
    # Return the resulting point list. If both polygons dont overlap, return the first one
    def Union(self, plist1, plist2, scale1=1.0, scale2=1.0):

        a = Polygon.Polygon(((self.GetContour(plist1))))
        b = Polygon.Polygon(((self.GetContour(plist2))))

        if (scale1 != 1.0):
            a.scale(scale1, scale1)
        if (scale2 != 1.0):
            b.scale(scale2, scale2)

        if (not a.overlaps(b)):
            return plist1

        c = a + b

        return self.GetPoint2DList(c)

    # Performs the difference operation between 2 Point2D object lists. Scale values are applied to each list to expand or reduce the polygons
    # Return a list with the resulting point lists. If both polygons dont overlap, return a list with the first one
    # Note that the returning list reason is that difference operation could produce more than one polygon
    def Difference(self, plist1, plist2, scale1=1.0, scale2=1.0):

        a = Polygon.Polygon(((self.GetContour(plist1))))
        b = Polygon.Polygon(((self.GetContour(plist2))))

        if (scale1 != 1.0):
            a.scale(scale1, scale1)
        if (scale2 != 1.0):
            b.scale(scale2, scale2)

        if (not a.overlaps(b)):
            return [plist1]

        c = a - b

        ret = []
        for contour in c:
            ret.append(self.GetPoint2DList([contour]))

        return ret

    # Giving a list of point2D objects lists (list of polygons), returns the largest one (the polygon with largest area)
    def GetLargestPolygon(self, lplist):

        maxArea = 0
        ret = None
        for pl in lplist:
            a = Polygon.Polygon(((self.GetContour(pl))))
            area = a.area()
            if (area > maxArea):
                maxArea = area
                ret = pl

        return ret

    # Return true if given Point2D lists overlaps
    def Overlaps(self, plist1, plist2):

        a = Polygon.Polygon(((self.GetContour(plist1))))
        b = Polygon.Polygon(((self.GetContour(plist2))))

        return a.overlaps(b)

    # Return true if one of the given Point2D lists covers absolutely the other
    def Covers(self, plist1, plist2):

        a = Polygon.Polygon(((self.GetContour(plist1))))
        b = Polygon.Polygon(((self.GetContour(plist2))))

        return (a.covers(b))

    # Clean repeated vertices or those that are too closer
    # DO NOT USE. FAILS LIKE A FAIR RIFLE ...
    def Clean(self, plist):

        a = Polygon.Polygon(((self.GetContour(plist))))
        return self.GetPoint2DList(Polygon.Utils.prunePoints(a))

    # Returns true if given point is inside given Point2D list
    def IsInside(self, plist, point):

        a = Polygon.Polygon(((self.GetContour(plist))))
        return a.isInside(point.x, point.y)

    # Returns true if given polygon is CCW
    def IsCCW(self, plist):

        a = Polygon.Polygon(((self.GetContour(plist))))
        b = a.orientation()[0]
        if (a.orientation()[0] == 1):
            return True
        else:
            return False
