import math

from Battles.Utils.Geometry import Segment2D, Ray2D, Vector2D, Point2D, Polygon2D, BoundingQuad
import Battles.Utils.Settings


class StarFortressData:
    """ Structure class where all  star fortress creation parameters are specified
    
    Attributes:
        BastionRadius: Bastion size (radius of circle used to construct it). Used only if initially towers are converted to bastions
        RavelinRadius: Radius of circle used to construct the ravelin (like in bastions)
        RavelinMinWidth: Minimum ravelin width. This avoids too thin ravelins
        HasHalfMoons: If half moons have to be calculated
        HalfMoonCircleOffset: Distance between halfmoon center and halfmoon circle radius
        HalfMoonLength: Distance from the halfmoon circle center to the halfmoon jag
        CovertWayThickness: Thickness of the covertway
        CovertWayOffset: Distance from the halfmoons and ravelins
        CovertWayPlacesOfArms: True if the places of arms (small triangles in each covertway non-convex angle) have to be created
        CovertWayPlacesOfArmsLength: Length of places of arms side
        GlacisThickness: Glacis width
    """

    def __init__(self):
        self.BastionRadius = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Bastion', 'VirtualCircleRadius')

        self.RavelinRadius = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'StarFortress', 'Ravelin/Radius')
        self.RavelinMinWidth = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'StarFortress', 'Ravelin/MinimumWidth')

        self.HasHalfMoons = Battles.Utils.Settings.SETTINGS.Get_B('Castle', 'StarFortress', 'HalfMoon/Active')
        self.HalfMoonCircleOffset = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'StarFortress',
                                                                          'HalfMoon/CircleOffset')
        self.HalfMoonLength = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'StarFortress', 'HalfMoon/Length')

        self.CovertWayThickness = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'StarFortress', 'CovertWay/Thickness')
        self.CovertWayOffset = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'StarFortress', 'CovertWay/Offset')
        self.CovertWayHasPlacesOfArms = Battles.Utils.Settings.SETTINGS.Get_B('Castle', 'StarFortress',
                                                                              'CovertWay/PlaceOfArms')
        self.CovertWayPlacesOfArmsLength = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'StarFortress',
                                                                                 'CovertWay/PlaceOfArmsLength')

        self.GlacisThickness = Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'StarFortress',
                                                                     'CovertWay/GlacisThickness')


class StarFortressElement:
    """ Helper class for StarFortress structure data. It contains a reference to a bastion, related ravelins and half-moon (see above)
    """

    def __init__(self):
        self.bastion = None
        self.leftRavelin = None  # Just think on the 2D view to know what are left and right sides
        self.rightRavelin = None
        self.halfMoon = None


class Ravelin:
    """ Fortress ravelin element. Its composed by a set of segments that draw a triangular shape (quasi triangle, in fact, is a 4 side polygon), with 2 frontal flanks and 2 small rear flanks
        It is placed between two bastions
        WARNING: Like bastions, the segments vertices order follows a path, from left to right, clockwise
    """

    def __init__(self):
        self.center = Point2D()
        self.leftFlank = Segment2D()
        self.rightFlank = Segment2D()
        self.leftRear = Segment2D()
        self.rightRear = Segment2D()

    def Draw(self, canvas, viewport):

        vp1 = viewport.W2V(self.leftFlank.p1)
        vp2 = viewport.W2V(self.leftFlank.p2)
        vp3 = viewport.W2V(self.rightFlank.p2)
        vp4 = viewport.W2V(self.rightRear.p2)
        canvas.create_line(vp1.x, vp1.y, vp2.x, vp2.y, fill="brown", width="2")
        canvas.create_line(vp2.x, vp2.y, vp3.x, vp3.y, fill="brown", width="2")
        canvas.create_line(vp3.x, vp3.y, vp4.x, vp4.y, fill="brown", width="2")
        canvas.create_line(vp4.x, vp4.y, vp1.x, vp1.y, fill="brown", width="2")

    def GetExternalShape(self):
        # Return the external shape in clockwise
        return [self.leftFlank, self.rightFlank]

    def GetSegmentList(self):

        return [self.leftFlank, self.rightFlank, self.leftRear, self.rightRear]

    def Intersect(self, obj):
        # Checks if any of current ravelin shape segments intersect with the given object
        # WARNING: Given object must to have implemented the GetSegmentList method
        # NOTE & TODO: Im noticed about it should be nice to create a parent class to manage ravelins and halfmoons, so the same method is present in both classes.
        #    Also, both objects have similar member data

        slist = self.GetSegmentList()
        sslist = obj.GetSegmentList()

        for ss in sslist:
            for s in slist:
                if s.Intersect(ss):
                    return True

        return False


class HalfMoon:
    """ Fortress halfmoon element. Its composed by to frontal flanks. The interior is cutted by a semicircle. Two small segments close the shape
        It is placed in front a bastion. It can be a separated structure, like ravelins, or can be integrated with the external wall (covert way) 
        WARNING: Like bastions, the segments vertices order follows a path, from left to right, clockwise
    """

    def __init__(self):
        self.center = Point2D()
        self.leftFlank = Segment2D()
        self.rightFlank = Segment2D()
        self.leftRear = Segment2D()
        self.rightRear = Segment2D()
        self.radius = 0.0

    def Draw(self, canvas, viewport):

        vp1 = viewport.W2V(self.leftFlank.p1)
        vp2 = viewport.W2V(self.leftFlank.p2)
        vp3 = viewport.W2V(self.rightFlank.p2)
        vp4 = viewport.W2V(self.rightRear.p2)
        vp5 = viewport.W2V(self.leftRear.p1)
        canvas.create_line(vp1.x, vp1.y, vp2.x, vp2.y, fill="brown", width="2")
        canvas.create_line(vp2.x, vp2.y, vp3.x, vp3.y, fill="brown", width="2")
        canvas.create_line(vp3.x, vp3.y, vp4.x, vp4.y, fill="brown", width="2")
        canvas.create_line(vp5.x, vp5.y, vp1.x, vp1.y, fill="brown", width="2")

        v1 = Vector2D().CreateFrom2Points(self.center, self.rightRear.p2)
        v2 = Vector2D().CreateFrom2Points(self.center, self.leftRear.p1)
        ang1 = v1.GetAngle()
        if (ang1 > 360.0):
            ang1 -= 360.0
        if (ang1 < 0.0):
            ang1 += 360.0
        ang2 = v2.GetAngle()
        if (ang2 > 360.0):
            ang2 -= 360.0
        if (ang2 < 0.0):
            ang2 += 360.0

        angbetween = v1.AngleBetween(v2)
        lastp = viewport.W2V(self.leftRear.p1)
        i = 0
        while (i < angbetween):
            p = Point2D()
            p.x = self.center.x + (self.radius * math.cos(math.radians(ang2)))
            p.y = self.center.y + (self.radius * math.sin(math.radians(ang2)))
            vp = viewport.W2V(p)
            canvas.create_line(lastp.x, lastp.y, vp.x, vp.y, fill="brown", width="2")

            # if (vp.Distance(lastp) > 1):
            #   a = 1

            lastp = vp
            ang2 += 1.0
            i += 1.0

    def GetExternalShape(self):
        # Return the external shape in clockwise
        return [self.leftFlank, self.rightFlank]

    def GetSegmentList(self):

        return [self.leftFlank, self.rightFlank, self.leftRear, self.rightRear]

    def Intersect(self, obj):
        # Checks if any of current ravelin shape segments intersect with the given object
        # WARNING: Given object must to have implemented the GetSegmentList method
        # NOTE & TODO: Im noticed about it should be nice to create a parent class to manage ravelins and halfmoons, so the same method is present in both classes.
        #    Also, both objects have similar member data

        slist = self.GetSegmentList()
        sslist = obj.GetSegmentList()

        for ss in sslist:
            for s in slist:
                if s.Intersect(ss):
                    return True

        return False


class CovertWay:
    """ The covert way is the set of external walls around the fortification
        The shape is a polygon with a shape fitted to the starfortress defensive elements, such are the ravelins and half moons
        The shape orientation is the same that the fortress shape elements: clockwise
    
        Attributes:
        
        IntShape: Internal wall shape
        ExtShape: External wall shape
        Thickness: Wall thick
        Offset: Distance from fortress elements
        Glacis: External shape around the covertway, or declivinity. This is a 2D shape, so the height slope is not considered here
        GlacisThickness: Glacis thickness from external shape
    """

    def __init__(self, data):
        # Given data is a StarFortreessData object
        self.intShape = Polygon2D()
        self.extShape = Polygon2D()
        self.thickness = data.CovertWayThickness
        self.offset = data.CovertWayOffset
        self.glacis = Polygon2D()
        self.glacisThickness = data.GlacisThickness

    def Draw(self, canvas, viewport):

        for s in self.intShape.shape:
            vp1 = viewport.W2V(s.p1)
            vp2 = viewport.W2V(s.p2)
            canvas.create_line(vp1.x, vp1.y, vp2.x, vp2.y, fill="orange", width="2")

        for s in self.extShape.shape:
            vp1 = viewport.W2V(s.p1)
            vp2 = viewport.W2V(s.p2)
            canvas.create_line(vp1.x, vp1.y, vp2.x, vp2.y, fill="orange", width="2")

        for s in self.glacis.shape:
            vp1 = viewport.W2V(s.p1)
            vp2 = viewport.W2V(s.p2)
            canvas.create_line(vp1.x, vp1.y, vp2.x, vp2.y, fill="gray", width="2")

    def GetExternalShape(self):
        # Return the external shape: the glacis or the covert way

        if (len(self.glacis.shape) > 1):
            return self.glacis.shape
        else:
            return self.extShape.shape


class StarFortress:
    """ Class to manage the set of construction objects of a star fortress. Walls, columns and bastions are not considered
    NOTE: All previous classes are helper and structure classes. All computations are made here
    
    Attributes:
        Castle: Reference to the interior castle
        Bastions: Dictionary with StarFortressElement objects that define the inside structure of fortress. The key is the bastion label
        Ravelins: Set of ravelins. A ravelin is a triangular (usually) construction placed between two bastions. 
        HalfMoons: Set of halfmoons. A halfmoon is a structure similar to ravelin and placed in front of the bastion. 
        CovertWay: External wall (see class definition to know more about it)
    """

    def __init__(self, castle, data=StarFortressData()):
        self.__castle = castle
        self.__bastions = {}
        self.__ravelins = []
        self.__halfMoons = []
        self.__covertWay = CovertWay(data)
        self.__data = data

    def SetData(self, data):
        self.__data = data
        self.__covertWay = CovertWay(data)

    def Create(self):
        # Construct the star fortress
        # Canvas parameter is used to update the draw of updated towers. Optional

        # The order of creation must be strict: Ravelins, halfmoons, and exterior wall
        self.__ConstructRavelins()
        if (self.__data.HasHalfMoons):
            self.__ConstructHalfMoons()
        self.__ConstructCovertWay()

    def __ConstructRavelins(self):

        self.__ravelins = []

        # The ravelin is constucted parametrically with bastion data and some constant values. It can be seen as two triangles, the bottom one, smaller, and the external, larger
        # The algorithm to get the ravelin center is:
        #    - Trace a segment between the bastion external vertices
        #    - Get the intersection between the two vectors related to the bastion flanks
        #    - Trace a wall perpendicular line from last intersection point. Get the intersection with the first segment. This is the center of the ravelin
        # The algorithm to get the front flanks is:
        #    - Trace a line from bastion vertices (those between front and rear flanks) at a constant angle value from the front flanks (never less than 90 degrees)
        #    - Get the lines intersection
        #    - Get the lines intersections with the first segment of previous algorithm
        #    - The external/front flanks are the segments between the intersection points
        # The algorithm to get the internal flanks is:
        #    - Trace a line from each previous intersection points at wall direction and with same front bastion flank
        #    - Get the intersection point between lines
        #    - The internal/rear flanks are the segments between the intersection points
        #
        #
        # But wait!. There are a problem with this algorithm. If the fortress is not symmetric, or the bastions are placed too far from each one, the ravelin becomes too large.
        # For that reason, a new method is defined 
        #
        # The method is the same, but not the flanks construction. In place of taking the bastion flank angle, choose a maximum distance from ravelin center and frontal vertex
        #
        # Finally, consider the ravelin shape segments to be constructed in the same direction than bastions, just to make it easy if in the future the ravelin shape must be queried
        #

        # Get each pair of castle bastions
        blist = self.__castle.GetBastionsList()
        if (not blist):
            return

        i = 0
        while (i < len(blist)):
            bastion1 = blist[i]
            if ((i + 1) >= len(blist)):
                bastion2 = blist[0]
            else:
                bastion2 = blist[i + 1]

            i += 1
            ravelin = Ravelin()

            # Calculate the ravelin center point
            flankseg1 = bastion1.GetFlankSegment(right=True, front=True)
            flankseg2 = bastion2.GetFlankSegment(right=False, front=True)

            bsegment = Segment2D(flankseg1.p1, flankseg2.p2)

            r1 = Ray2D(origin=flankseg1.p1, direction=flankseg1.GetDirection())
            r2 = Ray2D(origin=flankseg2.p2, direction=flankseg2.GetDirection().Invert())
            if (not r1.HitRay(r2)):
                print "ERROR: Ravelin cannot be constructed - code 1"
                continue

            r3 = Ray2D(origin=r1.GetHitPoint(),
                       direction=bastion2.GetFlankSegment(right=False, front=False).GetDirection())
            if (not r3.HitSegment(bsegment)):
                print "ERROR: Ravelin cannot be constructed - code 2"
                continue

            ravelin.center = r3.GetHitPoint()

            if (Battles.Utils.Settings.SETTINGS.Get_I('Castle', 'StarFortress', 'Ravelin/Method') == 1):
                # DEPRECATED!!!!
                # Calculate the front flanks

                # Rotate the bastion flanks segment vectors
                vec1 = flankseg1.GetDirection()
                vec1.Rotate(Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'StarFortress', 'Ravelin/BastionAngle'))
                vec2 = flankseg2.GetDirection()
                vec2.Rotate(-Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'StarFortress', 'Ravelin/BastionAngle'))

                # Intersect both vectors
                rr1 = Ray2D(origin=flankseg1.p2, direction=vec1)
                rr2 = Ray2D(origin=flankseg2.p1, direction=vec2)
                if (not rr1.HitRay(rr2)):
                    print "ERROR: Ravelin cannot be constructed - code 3"
                    continue

                ravelinexternalvertex = rr1.GetHitPoint()

                # Intersect each vector with ravelin base segment
                rr1.Reset()
                if (not rr1.HitSegment(bsegment)):
                    print "ERROR: Ravelin cannot be constructed - code 4"
                    continue
                if (not rr2.HitSegment(bsegment)):
                    print "ERROR: Ravelin cannot be constructed - code 5"
                    continue

                ravelin.leftFlank = Segment2D(rr1.GetHitPoint(), ravelinexternalvertex)
                ravelin.rightFlank = Segment2D(ravelinexternalvertex, rr2.GetHitPoint())

            elif (Battles.Utils.Settings.SETTINGS.Get_I('Castle', 'StarFortress', 'Ravelin/Method') == 2):

                # Extend the ravelincenter to defined radius

                ravelinexternalvertex = ravelin.center.Copy()
                vec = bastion2.GetFlankSegment(right=False, front=False).GetDirection()
                ravelinexternalvertex.Move(vec, self.__data.RavelinRadius)

                # Considering the segments between frontal vertex and previous bastion vertices, calculate the intersection points with the rays used to calculcate the ravelin center
                rrs1 = Ray2D(origin=ravelinexternalvertex,
                             direction=Vector2D().CreateFrom2Points(flankseg1.p2, ravelinexternalvertex))
                rrs2 = Ray2D(origin=ravelinexternalvertex,
                             direction=Vector2D().CreateFrom2Points(flankseg2.p1, ravelinexternalvertex))
                if (not rrs1.HitSegment(bsegment)):
                    print "ERROR: Ravelin cannot be constructed - code 6"
                    continue
                if (not rrs2.HitSegment(bsegment)):
                    print "ERROR: Ravelin cannot be constructed - code 7"
                    continue

                ravelin.leftFlank = Segment2D(rrs1.GetHitPoint(), ravelinexternalvertex)
                ravelin.rightFlank = Segment2D(ravelinexternalvertex, rrs2.GetHitPoint())


            else:
                print "ERROR: Ravelin method not defined"
                return

            # Finally, calculate the rear ravelin segments
            rb1 = Ray2D(origin=ravelin.leftFlank.p1, direction=flankseg1.GetDirection())
            rb2 = Ray2D(origin=ravelin.rightFlank.p2, direction=flankseg2.GetDirection().Invert())
            if (not rb1.HitRay(rb2)):
                print "ERROR: Ravelin cannot be constructed - code 10"
                continue
            ravelin.leftRear = Segment2D(rb1.GetHitPoint(), ravelin.leftFlank.p1)
            ravelin.rightRear = Segment2D(ravelin.rightFlank.p2, rb1.GetHitPoint())

            # A final check allow or not the ravelin construction if it is too small
            if (ravelin.rightRear.p1.Distance(ravelin.leftRear.p2) >= self.__data.RavelinMinWidth):

                self.__ravelins.append(ravelin)

                # Updates the starfortress structure
                if (not self.__bastions.has_key(bastion1.GetLabel())):
                    elem1 = StarFortressElement()
                    elem1.bastion = bastion1
                    elem1.rightRavelin = ravelin
                    self.__bastions[bastion1.GetLabel()] = elem1
                else:
                    self.__bastions[bastion1.GetLabel()].rightRavelin = ravelin

                if (not self.__bastions.has_key(bastion2.GetLabel())):
                    elem2 = StarFortressElement()
                    elem2.bastion = bastion2
                    elem2.leftRavelin = ravelin
                    self.__bastions[bastion2.GetLabel()] = elem2
                else:
                    self.__bastions[bastion2.GetLabel()].leftRavelin = ravelin

    def __ConstructHalfMoons(self):
        self.__halfMoons = []
        if (not self.__ravelins):
            print "ERROR: Cannot create the halfmoons without the previously calculated ravelins"
            return

        # The algorithm to create a half-moon follows a similar pattern than ravenlins, and needs some of their data  
        # From each bastion and related ravelins,
        #    - Trace 2 rays from frontal bastion flanks segments
        #    - Trace 2 rays from rear ravelin flanks segments, and intersect with the previous ones
        #    - From the segment between the two intersection points, get the mid point and apply a perpendicular movement to get the center of the inside circle
        #    - From the circle center, move in the same direction than bastion and at some constant value (could be the same distance used for ravelins jug calculation)
        #    - Trace to rays from already calculated jag in the same orientation than previous ravelin rays (but inverted direction)
        #    - Intersect the previous rays with the initial bastion rays
        #    - Construct the halfmoon flanks with the segments between previous intersection points and the jag (remember to consider the same orientation than ravelins and bastions)
        #    - Construct the interior halfcircle
        #    - Close the shape by adding small rear segments
        #
        # If there arent related ravelins the halfmoon cannot be constructed with this method. If there are only one, it can be constructed changing the initial steps:
        #    - Trace the bastion ray related with ravelin ray (first step of original algorithm, but only by one side)
        #    - Extend the other bastion segment the distance between intersected point and bastion jag
        #    - Construct the segment between both points
        #    - From here, the algorithm is the same
        #
        # NOTE: In fact, there are only two direction vectors to work, so the bastion flanks directions are the same than rear ravelin flanks directions (see ravelin code)
        #   

        # Get the list of bastions
        blist = self.__castle.GetBastionsList()
        if (not blist):
            return

        for bastion in blist:
            # Get the element with bastion and related ravelins
            if (not bastion.GetLabel() in self.__bastions):
                continue
            belement = self.__bastions[bastion.GetLabel()]
            if (not belement):
                continue

            halfmoon = HalfMoon()

            # Create the rays from bastion flanks and ravelins

            flankbastionright = bastion.GetFlankSegment(right=True, front=True)
            flankbastionleft = bastion.GetFlankSegment(right=False, front=True)
            brayleft = Ray2D(origin=flankbastionleft.p1, direction=flankbastionleft.GetDirection())
            brayright = Ray2D(origin=flankbastionright.p2, direction=flankbastionright.GetDirection())

            # There are only two vector directions that math with bastion flank directions
            leftvector = flankbastionleft.GetDirection()
            rightvector = flankbastionright.GetDirection().Invert()  # Note that both directions are focused to the bastion jag

            if (not belement.leftRavelin and not belement.rightRavelin):
                # Not enough data to construct the halfmoon
                continue

            elif (not belement.leftRavelin):

                rrayright = Ray2D(origin=belement.rightRavelin.leftRear.p1, direction=rightvector)

                # Intersect both rays
                if (not brayleft.HitRay(rrayright)):
                    print "ERROR: Halfmoon cannot be constructed - code 1"
                    continue

                halfmoon.rightRear.p2 = brayleft.GetHitPoint()

                # Extend the right bastion flank at same distance than ray hit from left flank
                dist = flankbastionleft.p2.Distance(halfmoon.rightRear.p2)
                halfmoon.leftRear.p1 = flankbastionright.p1.Copy()
                halfmoon.leftRear.p1.Move(rightvector, dist)


            elif (not belement.rightRavelin):

                rrayleft = Ray2D(origin=belement.leftRavelin.rightRear.p2, direction=leftvector)
                if (not brayright.HitRay(rrayleft)):
                    print "ERROR: Halfmoon cannot be constructed - code 2"
                    continue
                halfmoon.leftRear.p1 = brayright.GetHitPoint()

                # Extend the right bastion flank at same distance than ray hit from left flank
                dist = flankbastionright.p1.Distance(halfmoon.leftRear.p1)
                halfmoon.rightRear.p2 = flankbastionleft.p2.Copy()
                halfmoon.rightRear.p2.Move(leftvector, dist)


            else:

                rrayleft = Ray2D(origin=belement.leftRavelin.rightRear.p2, direction=leftvector)
                rrayright = Ray2D(origin=belement.rightRavelin.leftRear.p1, direction=rightvector)

                # Intersect each pair of rays
                if (not brayleft.HitRay(rrayright)):
                    print "ERROR: Halfmoon cannot be constructed - code 1"
                    continue
                if (not brayright.HitRay(rrayleft)):
                    print "ERROR: Halfmoon cannot be constructed - code 2"
                    continue

                halfmoon.leftRear.p1 = brayright.GetHitPoint()
                halfmoon.rightRear.p2 = brayleft.GetHitPoint()

            # Get the halfmoon center (the center of the interior circle) and radius
            baseseg = Segment2D(halfmoon.leftRear.p1, halfmoon.rightRear.p2)
            halfmoon.center = baseseg.GetMidPoint()
            halfmoon.center.Move(baseseg.GetNormal().Invert(), self.__data.HalfMoonCircleOffset)
            halfmoon.radius = halfmoon.center.Distance(halfmoon.leftRear.p1)

            # Get the frontal jag from center
            jag = halfmoon.center.Copy()
            jag.Move(baseseg.GetNormal(), self.__data.HalfMoonLength)

            # Calculate the flanks and close the shape
            frayleft = Ray2D(origin=jag, direction=leftvector.Copy().Invert())
            frayright = Ray2D(origin=jag, direction=rightvector.Copy().Invert())
            if (not frayleft.HitRay(brayright)):
                print "ERROR: Halfmoon cannot be constructed - code 3"
                continue
            if (not frayright.HitRay(brayleft)):
                print "ERROR: Halfmooon cannot be constructed - code 4"
                continue

            halfmoon.leftRear.p2 = frayleft.GetHitPoint()
            halfmoon.rightRear.p1 = frayright.GetHitPoint()
            halfmoon.leftFlank = Segment2D(halfmoon.leftRear.p2, jag)
            halfmoon.rightFlank = Segment2D(jag, halfmoon.rightRear.p1)

            # Before adding the halfmoon, check if it intersects any other ravelin. This could happens if the castle shape is strange or there are too much distance between bastions
            error = False
            for rv in self.__ravelins:
                if (rv.Intersect(halfmoon)):
                    print "ERROR: Halfmoon cannot be constructed - code 5"
                    error = True
                    break

            if (not error):
                for hm in self.__halfMoons:
                    if (hm.Intersect(halfmoon)):
                        print "ERROR: Halfmoon cannot be constructed - code 6"
                        error = True
                        break

                if (not error):
                    self.__halfMoons.append(halfmoon)
                    self.__bastions[bastion.GetLabel()].halfMoon = halfmoon

            """
            self.__halfMoons.append(halfmoon)                    
            self.__bastions[bastion.GetLabel()].halfMoon = halfmoon
            """

    def __ConstructCovertWay(self):

        # The algorithm here is simple:
        # - Get all external shapes from ravelins and halfmoons
        # - Offset all of them by a constant value
        # - Convert them into rays and intersect alltogether (pair by pair)
        # - Expand the shape by thickness to get the external shape
        # - If places of arms constructions are activated, create a small triangle for each non-convex angle of external shape
        # - Expand the final shape to get the glacis

        # Get the external shapes in bastion order
        blist = self.__castle.GetBastionsList()  # TODO: Check and make sure that returned list is in geometric order, in clockwise around the castle

        poly = Polygon2D()

        if (not self.__ravelins):
            print "ERROR: The covert way cannot be constructed without ravelin data"
            return

        if (not self.__halfMoons):
            # We need to expand the bastion flanks to be merged with the ravelin flanks and create the outline wall
            # To calculate the distance of the gateway between bastion and ravelins, intersect the bastion flank normal vector with the related ravelin rear flank vector

            # Use the first bastion with right ravelin (or left, anyway)
            # Use the right bastion flank (or the left, anyway)
            i = 0
            found = False
            while ((i < len(blist) and not found)):
                belement = self.__bastions[blist[i].GetLabel()]
                if (belement.rightRavelin):
                    brightseg = belement.bastion.GetFlankSegment(right=True, front=True)
                    r1 = Ray2D(origin=brightseg.GetMidPoint(), direction=brightseg.GetNormal())
                    r2 = Ray2D(origin=belement.rightRavelin.leftRear.p1,
                               direction=belement.rightRavelin.leftRear.GetDirection())
                    if (not r1.HitRay(r2)):
                        continue

                    bastionoffset = brightseg.GetMidPoint().Distance(r1.GetHitPoint())

                    found = True

                i += 1
            if (not found):
                print "ERROR: The covert way cannot be constructed - Not enough ravelin and bastion data"

            # Construct the polygon with ravelin and bastion data
            for b in blist:
                belement = self.__bastions[b.GetLabel()]

                bflankleft = b.GetFlankSegment(right=False, front=True).Copy()
                bflankright = b.GetFlankSegment(right=True, front=True).Copy()
                bflankleft.Move(direction=bflankleft.GetNormal(), distance=bastionoffset)
                bflankright.Move(direction=bflankright.GetNormal(), distance=bastionoffset)

                poly.shape.extend([bflankleft, bflankright])

                if (belement.rightRavelin):
                    poly.shape.extend(belement.rightRavelin.GetExternalShape())




        else:

            # Construct the polygon with ravelin and halfmoon data
            for b in blist:

                if (not b.GetLabel() in self.__bastions):
                    continue

                belement = self.__bastions[b.GetLabel()]

                if (belement.halfMoon):
                    poly.shape.extend(belement.halfMoon.GetExternalShape())
                else:

                    # If the bastion doesnt have previous ravelin, and the bastion isnt enough large, some artifacts can appear crossing the projected bastion lines
                    if (belement.leftRavelin):
                        bflankleft = b.GetFlankSegment(right=False, front=True).Copy()
                        bflankright = b.GetFlankSegment(right=True, front=True).Copy()
                        # bflankleft.Move(direction = bflankleft.GetNormal(), distance = bastionoffset)
                        # bflankright.Move(direction = bflankright.GetNormal(), distance = bastionoffset)

                        poly.shape.extend([bflankleft, bflankright])

                if (belement.rightRavelin):
                    poly.shape.extend(belement.rightRavelin.GetExternalShape())

        # Expand the polygon to get the interior covert way shape
        poly.Expand(self.__covertWay.offset)

        # Remove those too short segments to avoid artifacts
        poly.PurgeShortSegments(
            Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'StarFortress', 'CovertWay/MinimumSegmentLength'))

        self.__covertWay.intShape = poly

        # Expand the internal shape by wall thickness
        poly2 = poly.Copy()
        poly2.Expand(self.__covertWay.thickness)
        poly2.PurgeShortSegments(
            Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'StarFortress', 'CovertWay/MinimumSegmentLength'))

        self.__covertWay.extShape = poly2

        # Expand the final external shape to create the glacis
        poly3 = self.__covertWay.extShape.Copy()
        poly3.Expand(self.__covertWay.glacisThickness)
        poly3.PurgeShortSegments(
            Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'StarFortress', 'CovertWay/MinimumSegmentLength'))

        self.__covertWay.glacis = poly3

        # Create the places of arms
        if (self.__data.CovertWayHasPlacesOfArms):
            self.__CreatePlacesOfArmsOnCovertWay()

    def __CreatePlacesOfArmsOnCovertWay(self):

        # The algorithm follows next steps:
        #    - Search all non-convex vertices
        #    - For each one, creates 2 new vertices, one for each related segment, at constant length from the vertex
        #    - From the new vertices trace 2 rays parallel to the opposite segments
        #    - Get the intersection point as the place jag
        #    - Remove the non-convex vertex and update the polygon
        #

        poly = self.__covertWay.extShape.Copy()
        self.__covertWay.extShape = Polygon2D()

        i = 0
        while (i < len(poly.shape)):
            s1 = poly.shape[i]
            if ((i + 1) == len(poly.shape)):
                inext = 0
            else:
                inext = i + 1
            s2 = poly.shape[inext]

            # Check the convexity
            if (s1.ConvexTo(s2) or (s1.GetLength() <= self.__data.CovertWayPlacesOfArmsLength) or (
                    s2.GetLength() <= self.__data.CovertWayPlacesOfArmsLength)):
                self.__covertWay.extShape.shape.append(s1)
            else:

                # Create the place of arms

                # Left side
                pleft = s1.p2.Copy()
                pleft.Move(s1.GetDirection().Invert(), self.__data.CovertWayPlacesOfArmsLength)

                # Right side
                pright = s1.p2.Copy()
                pright.Move(s2.GetDirection(), self.__data.CovertWayPlacesOfArmsLength)

                # Jag
                rleft = Ray2D(origin=pleft, direction=s2.GetDirection())
                rright = Ray2D(origin=pright, direction=s1.GetDirection().Invert())
                if (not rleft.HitRay(rright)):
                    print "ERROR: Cannot create the place of arms"
                    i += 1
                    continue
                jag = rleft.GetHitPoint()

                # Get the new segments
                ss1 = Segment2D(s1.p1, pleft)
                sleft = Segment2D(pleft, jag)
                sright = Segment2D(jag, pright)
                ss2 = Segment2D(pright, s2.p2)

                # Update the shape
                self.__covertWay.extShape.shape.extend([ss1, sleft, sright])

                # The last segment cannot be updated yet, so we need to check the convexity with the next segment
                poly.shape[inext] = ss2
                if (inext == 0):
                    self.__covertWay.extShape.shape[0] = ss2

            i += 1

    def Draw(self, canvas, viewport):

        for r in self.__ravelins:
            r.Draw(canvas, viewport)

        for r in self.__halfMoons:
            r.Draw(canvas, viewport)

        self.__covertWay.Draw(canvas, viewport)

    def GetBounding(self):

        if (not self.__ravelins):
            return None

        bound = BoundingQuad()

        for r in self.__ravelins:
            shape = r.GetExternalShape()
            for s in shape:
                bound.InsertPoint(s.p1)
                bound.InsertPoint(s.p2)

        for r in self.__halfMoons:
            shape = r.GetExternalShape()
            for s in shape:
                bound.InsertPoint(s.p1)
                bound.InsertPoint(s.p2)

        shape = self.__covertWay.GetExternalShape()
        for s in shape:
            bound.InsertPoint(s.p1)
            bound.InsertPoint(s.p2)

        return bound
