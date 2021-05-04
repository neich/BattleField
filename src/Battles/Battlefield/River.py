
from Battles.Utils.Geometry import Point2D, Polygon2D, Segment2D, Vector2D, BoundingQuad



class River:
    """ Class to define a river on the battlefield. It is defined by a polyline with a width. The polyline is expanded on the battlefield by its width
        The battlefield cells that match with the river are marked as river cells. This kind of cells share the same functionality than moat cells
        
        Attributes: 
        
            - Width: River width (constant)
            - Axis: 2D polyline that defines the river placement and direction
            - Shape: 2D polygon with the river shape. Constructed automatically from a polyline and its bounding
            - BattlefieldCells: List of cells that match with the river
            - right/leftCap: Triangular caps to get a smooth transition between rivers
            
    """
    
    def __init__(self, width, polyline):
        # Given polyline is used to create a bounding polygon around it. It is a list of 2D points
        self.__width = width
        self.__shape = Polygon2D()
        
        self.__battlefieldCells = []
        
        self.__canvasObjs = []          # Internal list of drawn objects
        self.__axis = polyline

        self.__rightCap = Polygon2D()
        self.__leftCap = Polygon2D()

        self.__CreateShape(polyline)



    
    def GetWidth(self):
        return self.__width
    
    
    def __CreateShape(self, polyline):
    
        # Expand the polyline with the current width to construct a bounding polygon

        # Calculate the set of vectors to expand the polyline vertices
        # For the first and last vertices we use the perpendicular vectors. For the others, the bisector 
        
        if (len(polyline) < 2):
            print "ERROR: Given polyline is not enough to construct the river"
            return
        
        vecs = [Segment2D(polyline[0], polyline[1]).GetNormal()]

        i = 1
        while (i < (len(polyline) - 1)):
            v1 = Vector2D().CreateFrom2Points(polyline[i-1], polyline[i])
            v1.Rotate(-90)
            v2 = Vector2D().CreateFrom2Points(polyline[i], polyline[i+1])
            v2.Rotate(-90)
            vecs.append(v1.Bisector(v2))
            i += 1
    
        vecs.append(Segment2D(polyline[-2], polyline[-1]).GetNormal())
        
        # Move each polyline vertex using the vectors to get the polygon set of segments
        
        # Top edge (there isnt any top or bottom, its just an orientative consideration)
        i = 0
        plast = Point2D()
        while (i < len(polyline)):
            p = polyline[i].GetMove(vecs[i], self.__width)
            if (i > 0):
                self.__shape.shape.append(Segment2D(plast, p))
            plast = p
            i += 1

        # Right edge
        p1 = polyline[-1]
        p2 = p1.Copy()
        self.__shape.shape.append(Segment2D(p1.GetMove(vecs[-1], self.__width), p2.GetMove(vecs[-1], -self.__width)))

        # Right triangular cap
        seg = self.__shape.shape[-1]
        pcap = polyline[-1].Copy()
        pcap.Move(Vector2D().CreateFrom2Points(polyline[-2],polyline[-1]), self.__width)
        self.__rightCap.shape.append(seg.Copy())
        self.__rightCap.shape.append(Segment2D(seg.p2.Copy(), pcap))
        self.__rightCap.shape.append(Segment2D(pcap, seg.p1.Copy()))

        # Bottom edge
        i = len(polyline) - 1
        while (i >= 0):
            p = polyline[i].GetMove(vecs[i], -self.__width)
            if (i < (len(polyline) - 1)):
                self.__shape.shape.append(Segment2D(plast, p))
            plast = p
            i -= 1
            
        # Left edge
        p1 = polyline[0]
        p2 = p1.Copy()
        self.__shape.shape.append(Segment2D(p1.GetMove(vecs[0], -self.__width), p2.GetMove(vecs[0], self.__width)))

        # Left triangular cap
        seg = self.__shape.shape[-1]
        pcap = polyline[0].Copy()
        pcap.Move(Vector2D().CreateFrom2Points(polyline[1],polyline[0]), self.__width)
        self.__leftCap.shape.append(seg.Copy())
        self.__leftCap.shape.append(Segment2D(seg.p2.Copy(), pcap))
        self.__leftCap.shape.append(Segment2D(pcap, seg.p1.Copy()))

        
    def GetBounding(self):
        # Returns the river shape 2D bounding
        
        bound = BoundingQuad()
    
        for s in self.__shape.shape:
            bound.InsertPoint(s.p1)
            # The shape is closed, so considering only the first segment point is enough
    
        return bound
    
    
    def IsInside(self, point):
        # Return true if given point is inside the river
        if (self.__shape):
            return self.__shape.IsInside(point)
        else:
            return False
        
        
        
    def AddBattlefieldCell(self, cell):
        self.__battlefieldCells.append(cell)
        
        
        
        
    def Draw(self, canvas, viewport):

        if (len(self.__canvasObjs) > 0):
            for c in self.__canvasObjs:
                canvas.delete(c)

        color = "PowderBlue"

        '''
        for c in self.__battlefieldCells:
            bbox = c.GetBoundingQuad()
            vp1 = viewport.W2V(bbox.minPoint)
            vp2 = viewport.W2V(bbox.maxPoint)
            self.__canvasObjs.append(canvas.create_rectangle(vp1.x, vp1.y, vp2.x, vp2.y, fill=color, outline = color))

        for s in self.__shape.shape:
            
            vp1 = viewport.W2V(s.p1)
            vp2 = viewport.W2V(s.p2)
            self.__canvasObjs.append(canvas.create_line(vp1.x, vp1.y, vp2.x, vp2.y, fill = "black"))
        '''

        lst = []
        for s in self.__shape.shape:
            vp1 = viewport.W2V(s.p1)
            vp2 = viewport.W2V(s.p2)
            lst.append(vp1.x)
            lst.append(vp1.y)
            lst.append(vp2.x)
            lst.append(vp2.y)
        self.__canvasObjs.append(canvas.create_polygon(lst, fill=color, outline=color))

        lst = []
        for s in self.__rightCap.shape:
            vp1 = viewport.W2V(s.p1)
            vp2 = viewport.W2V(s.p2)
            lst.append(vp1.x)
            lst.append(vp1.y)
            lst.append(vp2.x)
            lst.append(vp2.y)
        self.__canvasObjs.append(canvas.create_polygon(lst, fill=color, outline=color))

        lst = []
        for s in self.__leftCap.shape:
            vp1 = viewport.W2V(s.p1)
            vp2 = viewport.W2V(s.p2)
            lst.append(vp1.x)
            lst.append(vp1.y)
            lst.append(vp2.x)
            lst.append(vp2.y)
        self.__canvasObjs.append(canvas.create_polygon(lst, fill=color, outline=color))



        
    def GetClosestAxisSegment(self, point):
        # Returns the closest axis segment to given point
        
        mindist = float('inf')
        seg = None
        
        i = 0
        while (i < len(self.__axis)):

            s = Segment2D(self.__axis[i-1], self.__axis[i])
            dist = s.DistanceToPoint(point)
            if (dist < mindist):
                seg = s
                mindist = dist
                
            i += 1
            
        return seg        
                
        
        
    def IntersectAxis(self, segment):
        # Returns the intersection point between given segment and any river axis segment, or none
        
        i = 0
        while (i < len(self.__axis)):

            s = Segment2D(self.__axis[i-1], self.__axis[i])
            pnt = s.Intersect(segment)
            if (pnt != None): 
                return pnt
            i += 1
            
        return None
        
        
        
    def GetPointsList(self):
        # Returns the shape in a Point2D list

        return self.__shape.GetPointsList()
        
                
        