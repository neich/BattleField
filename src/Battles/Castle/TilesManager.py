import math
import random


from Battles.Utils.Geometry import Point2D, Vector2D, Point3D, Vector3D, Segment2D
import Battles.Utils.Settings 



class Tile:
    """ Basic tile class
    
    Attributes:
        statusVal: Current status value for tile. It decreases as receive shoots. 0 value means a destroyed tile
        index: Tile indices 
        
    """
    
    def __init__(self, value, row, column):
        
        self.statusVal = value
        self.index = {"row": row, "column": column}
        
        
    def IsHole(self):  
        return (self.statusVal <= 0)
            




class TilesManager:
    """ Tiles manager class. It controls the tiles for a specific construction (only walls currently ... )
        Also controls the holes and rubble produced by the tiles destruction
    
    
    Attributes:
        construction: Related construction (only walls currently TODO: Allow more construction types)
        rubble: list to store the rubble amount in front of wall produced by cannon hits. There is "a rubble" amount for each tile column. O means no rubble. For each
                fallen tile, the respective rubble slot is increased by a tile height percentage (see defaults). The rubble slots are used to allow start climbing at higher positions (or to enter
                to the castle without effort)
        rubbleHeightSteps: List of rubble height increases per fallen tile level. That is, for each row, the same amount of rubble will fail for all columns. These values are
                    precalculated to be used when a tile falls
        tiles: Array representing the construction tiles (where tiles are avaiable). A tile is only a resistance number (the tile shape can be calculated from array indices and construction dimensions)
        tilesSize: Array size
        tileDims: Tile dimensions
        tileResistance: Tile resistance material. Comparable with troops attack values
        gateways: List of column indices that have gateways, that is a way to pass trough the wall without climbing and helped by the rubble
    """
    
    def __init__(self, construction):
        
        self.__construction = construction
        
        self.__tiles = []
        self.__tilesSize = {"rows": 0, "columns": 0}
        self.__tileDims = {"width":  Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Wall', 'Tile/Width'), "height":  Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Wall', 'Tile/Height')}
        self.__tileResistance =  Battles.Utils.Settings.SETTINGS.Get_F('Castle', 'Wall', 'Tile/Resistance')
       
        self.__rubble = []
        self.__rubbleHeightSteps = []
       
        self.__gateways = []
        
        
        
        
    def Reset(self):
        # Restore tiles
        self.__tiles = []
        i = 0
        while (i < self.__tilesSize["rows"]):
            j = 0
            row = []
            while (j < self.__tilesSize["columns"]):
                row.append(Tile(self.__tileResistance, i, j))
                j += 1
            self.__tiles.append(row)
            i += 1

        self.__rubble = []
        self.__gateways = []
        
        
        
    def RecalculateTiles(self):    
               
        l = self.__construction.GetLength()
        del self.__tiles[0:len(self.__tiles)]

        tcols = math.ceil(l / self.__tileDims["width"])    # The last tile in each row will be smaller 
        trows = math.ceil(self.__construction.GetHeight() / self.__tileDims["height"])    # The last tile row will be shorter

        i = 0
        while (i < trows):
            j = 0
            row = []
            while (j < tcols):
                row.append(Tile(self.__tileResistance, i, j))
                j += 1
            self.__tiles.append(row)
            i += 1
        self.__tilesSize["rows"] = trows
        self.__tilesSize["columns"] = tcols
        
        # Inits the rubble
        self.__rubble = []
        i = 0
        while (i < tcols):
            self.__rubble.append(0)
            i += 1

        self.__gateways = []
        
        # Recalculate the rubble height steps
        self.__rubbleHeightSteps = []

        # To calculate the amount of tile converted to rumble we consider a wedge with a volume equal to the fallen rubbles!!!
		# the length is the same for the tile and the rubbles, so it is simplified from the equations. 
		# The area of tile that falls must be equal to a ground rectangle triangle area, with equal sides. To calculate the value of this side,
        #
        # Equal sides -> A = b^2 / 2
        # If we equal both areas, b^2 / 2 = wallthick * tileheight   <== Was wallthink/2, but it is not correct
        # So, b = sqrt(2 * wallthic * tileheight)
        #
        # Now, considering the accumulation
        # The rubble converts the triangle rectangle with equal sides (b1) to another triangle rectangle with equal sides (b2)
        # Then, A2 = A1 + A1 = 2 * (b1^2 / 2) = b2^2/2 = 2 * wallthick * tileheight
        # So, b2 = sqrt(2 * 2 * wallthick * tileheight)
        # Extending it to next  tile falls, bn = sqrt(Sum * 2 * wallthick * tileheight) = sqrt(n * 2 * wallthick * tileheight)
        # Note that "n" value is the number of fallen tiles, and all are the same dimensions



        self.__rubbleHeightSteps.append(0)
        nfallen = 1
        accum = 0
        while (nfallen <= self.__tilesSize["rows"]):
            self.__rubbleHeightSteps.append(math.sqrt(nfallen * 2 * self.__construction.GetThickness() * self.__tileDims["height"]) - accum)
            accum += self.__rubbleHeightSteps[-1]
            nfallen += 1

        
        
    def SetResistance(self, r):
        self.__tileResistance = r
    
 
  
    def GetBestTileToShoot(self, frompos):
        # Returns the tile that is the best suitable tile to shoot from given position
        # Due the goal is to create a gateway for the soldiers, the cannons try to shoot at higher wall positions. Due all tiles are placed at same xy pos, get the best
        # tile "column", and then the highest one
        
        pos2D = Point2D().SetFrom3D(frompos)
        
        ret = {"row": -1, "column": -1}
        maxD = -1.0
        
        normal = self.__construction.GetNormalVector()

        # Do a two pass search. First, search for the best tile to shoot without any hole at left or right. Second, just search the best tile to shoot if previous search failed
        # This avoid launching rubble to left and right of already holes. Otherwise, the rubble could cover the hole, and make it higer
        end = False
        firstpass = True
        while (not end):
            j = 0
            while (j < self.__tilesSize["columns"]):

                # Check for rubble status
                nrubbletiles = self.GetNRubbleCoveredTiles(j)

                # Check if there are any tile to shoot
                i = nrubbletiles
                found = False
                if (firstpass):
                    # Check for left and right hole condition
                    while (not found and (i < self.__tilesSize["rows"])):

                        if (i > 0):
                            left = self.__tiles[i-1][j].IsHole()
                        else:
                            left = False
                        center = self.__tiles[i][j].IsHole()
                        if (i < (self.__tilesSize["rows"] - 1)):
                            right = self.__tiles[i+1][j].IsHole()
                        else:
                            right = False

                        if (left or right or center):
                            i += 1
                        else:
                            found = True
                else:
                    while (not found and (i < self.__tilesSize["rows"])):
                        if (not self.__tiles[i][j].IsHole()):
                            found = True
                        else:
                            i += 1

                if (found):

                    center = self.GetTileCenter(self.__tiles[i][j])

                    # Because we don't worry about the cannon height, calculate the distances only in 2D
                    # TODO: Calculate it in 3D space to be more accurate
                    center2D = Point2D().SetFrom3D(center)

                    dist = center2D.Distance(pos2D)

                    invec = Vector3D()
                    invec.CreateFrom2Points(Point3D().SetFrom2D(center2D), Point3D().SetFrom2D(pos2D))
                    anglefactor = invec.DotProd(normal)

                    # Greater distance -> less effective
                    # Near to wall normal -> more effective
                    factor = anglefactor / dist

                    if (factor > maxD):
                        maxD = factor
                        ret["column"] = j

                j += 1

            if (maxD != -1):
                end = True                  # Found the best one (first or second pass)
            else:
                if (firstpass):
                    firstpass = False       # Not found. Launch the second pass
                else:
                    end = True              # Not found. End of second pass

           
        # Check another amazing case (no wall!)
        if (maxD == -1):
            return None
        else:
            
            # Get the tallest row. Remember to consider the holes and the rubble
            nrubbletiles = self.GetNRubbleCoveredTiles(ret["column"])
            
            i = int(self.__tilesSize["rows"] - 1)
            while ((i >= nrubbletiles) and self.__tiles[i][ret["column"]].IsHole()):
                i -= 1
                
            ret["row"] = i
            
            return self.__tiles[ret["row"]][ret["column"]]
        
            

        
    def GetTileCenter(self, tile):
        # Returns the 3D center of given tile 
        # Note that this is the real position, not local wall position
        
        vector = Vector2D()
        vector.CreateFrom2Points(self.__construction.GetStartPosition(), self.__construction.GetEndPosition())
        
        pos = self.__construction.GetStartPosition().Copy()
        pos.Move(vector, (self.__tileDims["width"] * tile.index["column"]) + (self.__tileDims["width"] / 2))
        
        height = (tile.index["row"] * self.__tileDims["height"]) + (self.__tileDims["height"] / 2) 
        
        
        return Point3D(pos.x, pos.y, height)



    def IsTopTile(self, tile):
        # Returns true if given tile is on the top of wall
        return (tile.index["row"] == (self.__tilesSize["rows"] - 1))
        
        
    def GetTileWallDistance(self, tile):
        # Returns the given tile distances to construction start position
        # The returned value is a dictionary with distance from starting tile position and from ending tile position
        
        ret = {"distance1": self.__tileDims["width"] * tile.index["column"], "distance2": 0}

        ret["distance2"] = ret["distance1"] + self.__tileDims["width"]
        
        return ret
    
    
        
    def GetNearestHolePosition(self, frompos):
        # Returns the nearest hole position, that is the central tile point of the nearest 0 tile value
        
        minD = -1
        posMin = Point3D()
        
        i = 0
        while (i < self.__tilesSize["rows"]):
            j = 0
            while (j < self.__tilesSize["columns"]):
                if (self.__tiles[i][j].IsHole()):
                    center = self.GetTileCenter(self.__tiles[i][j])
                    dist = center.Distance(frompos)
                    if ((dist < minD) or (minD == -1)):
                        minD = dist
                        posMin = center
                j += 1
            i += 1
            
        if (minD == -1):
            return None
        else:
            return posMin
        
        
            
        
       
     
    def GetTile(self, pos):
        # Return the tile that matches with given 3D position
        
        startpos = self.__construction.GetStartPosition()
        #dist = startpos.Distance(pos)
        xdist = Point2D().SetFrom3D(startpos).Distance(Point2D().SetFrom3D(pos))
        row = int(math.floor(pos.z / self.__tileDims["height"]))
    
        if (row >= self.__tilesSize["rows"]):
            row = int(self.__tilesSize["rows"] - 1)
    
        column = int(math.floor(xdist / self.__tileDims["width"]))
        
        if (column >= self.__tilesSize["columns"]):
            column = int(self.__tilesSize["columns"] - 1)
         
        return self.__tiles[row][column]
        
          
        
    def IsInHole(self, pos):
        # Returns true if given position is on a hole tile
        
        tile = self.GetTile(pos)
        return tile.IsHole()
   
    
    
  
    
    
    def GetHolesSegmentList(self):
        # Return a list of 2D segments over the wall and on the holes (if any)
        ret = []
        
        wallvec = self.__construction.GetWallVector()
        startpos = self.__construction.GetStartPosition()
        
        j = 0
        while(j < self.__tilesSize["columns"]):
            
            i = int(self.__tilesSize["rows"] - 1)
            found = False
            while ((i >= 0) and not found):
                
                if (self.__tiles[i][j].IsHole()):
                    found = True

                    p1 = startpos.Copy()
                    p1.Move(wallvec, j * self.__tileDims["width"])
                    p2 = p1.Copy()
                    p2.Move(wallvec, self.__tileDims["width"])
                    seg = Segment2D(p1, p2)
                    ret.append(seg)
                
                i -= 1
            
            j += 1
            
        return ret
    


    def GetGatewaySegmentList(self):
        # Return a list of 2D segments over the wall and on the gateways (if any)
        ret = []
        
        wallvec = self.__construction.GetWallVector()
        startpos = self.__construction.GetStartPosition()
        
        for j in self.__gateways:
            
            p1 = startpos.Copy()
            p1.Move(wallvec, j * self.__tileDims["width"])
            p2 = p1.Copy()
            p2.Move(wallvec, self.__tileDims["width"])
            seg = Segment2D(p1, p2)
            ret.append(seg)
            
        return ret

    
     
        
    def GetRubbleHeight(self, position):
        # Returns the rubble height (if any) on given 3D position
            
        # Get the tile column to know the rubble slot
        p = Point2D().SetFrom3D(position)
        distx = p.Distance(self.__construction.GetStartPosition())
        col = int(math.floor(distx / self.__tileDims["width"]))

        if (col >= len(self.__rubble)):
            col = len(self.__rubble) - 1        # This should never happen

        return self.__rubble[col]
        
           
    
    
    
    def RayHit(self, ray):
        # Tests the ray hit over the tiles and return, if any, the intersected tile
        
        # Horizontal distance (discard z value)
        p0 = Point2D()
        p0.SetFrom3D(ray.GetHitPoint())
        distx = p0.Distance(self.__construction.GetStartPosition())
        
        # Vertical distance, distance from ground
        disty = ray.GetHitPoint().z
        
        row = int(math.floor(disty / self.__tileDims["height"]))
        col = int(math.floor(distx / self.__tileDims["width"]))
        
        # Update the tile resistance
        # The ray energy must be reduced by the impact angle
        tile = self.__tiles[row][col]
        tile.statusVal -= int(ray.GetCosEnergy(self.__construction.GetNormalVector()))
        if (tile.IsHole()):
            tile.statusVal = 0


            # Update the rubble
			# The calculation is done above!
			# Finally, we take into consideration the rumble that falls on sides (its not accumultive)
			# To solve we need to calculate the difference between different rumble levels and accumulate it

            torubble = Battles.Utils.Settings.SETTINGS.Get_A('Castle', 'Wall', 'Tile/RubbleConversionFactor')

            # Update current column rubble
            nfallen = self.GetNFallenTilesByColumn(col)
            self.__rubble[col] += self.__rubbleHeightSteps[nfallen] * torubble[1]

            # Update side columns rubble
            if (col == 0):
                self.__rubble[col] += self.__rubbleHeightSteps[nfallen] * torubble[0]       # If there are not left column, accumulate its rumble to the current one
            else:
                self.__rubble[col-1] += self.__rubbleHeightSteps[nfallen] * torubble[0]

            if (col == (self.__tilesSize["columns"] - 1)):
                self.__rubble[col] += self.__rubbleHeightSteps[nfallen] * torubble[2]       # If there are not right column, accumulate its rumble to the current one
            else:
                self.__rubble[col+1] += self.__rubbleHeightSteps[nfallen] * torubble[2]


            # Check if any gateway has been created
            rubbletile = self.GetRubbleTile(col)
            if (rubbletile and rubbletile.IsHole() and (col not in self.__gateways)):
                self.__gateways.append(col)
                
            if (col > 0):
                leftrubbletile = self.GetRubbleTile(col-1)
                if (leftrubbletile and leftrubbletile.IsHole() and ((col-1) not in self.__gateways)):
                    self.__gateways.append(col-1)
            
            if (col < (self.__tilesSize["columns"] - 1)):
                rightrubbletile = self.GetRubbleTile(row-1)
                if (rightrubbletile and rightrubbletile.IsHole() and ((col+1) not in self.__gateways)):
                    self.__gateways.append(col+1)
            
            

        return tile
            


    def GetNFallenTilesByColumn(self, col):
        # Return the number of fallen tiles of given column

        count = 0
        row = int(self.__tilesSize["rows"]) - 1
        while ((row >= 0) and self.__tiles[row][col].IsHole()):
            count += 1
            row -= 1

        return count




    
    def GetRubbleTile(self, column):        
        # Return the last tile that is covered by the rubble at given column

        if ((column < 0) or (column >= len(self.__rubble))):
            return None

        if (self.__rubble[column] < self.__tileDims["height"]):
            return None
        
        row = int(math.floor(self.__rubble[column] / self.__tileDims["height"])) 
        
        if (row >= self.__tilesSize["rows"]):
            row = int(self.__tilesSize["rows"] - 1)
        
        return self.__tiles[row][column]
        
     
    def GetNRubbleCoveredTiles(self, column):
        # Return the number of covered tiles by rubble on given indexed column
        
        return int(math.floor(self.__rubble[column] / self.__tileDims["height"]))




    def IsWallFallen(self):
        # Returns true if all tiles are broken or occluded by the rubble
        
        j = 0
        while (j < self.__tilesSize["columns"]):
                 
            i = int(math.floor(self.__rubble[j] / self.__tileDims["height"]))
            while (i < self.__tilesSize["rows"]):
                if (not self.__tiles[i][j].IsHole()):
                    return False
                i += 1
            j += 1
            
        return True    
            
            
            
            


    def DrawTiles(self, canvas, viewport):
        
        # Draw the tiles into a height view. Return the created canvas objects
        
        ret = []
        
        wheight = self.__construction.GetHeight()       
        wlength = self.__construction.GetLength()        
                
        i = 0
        while (i < self.__tilesSize["rows"]):
            j = 0
            while (j < self.__tilesSize["columns"]):
               
                if ((i + 1) == self.__tilesSize["rows"]):
                    offsetY = wheight - (i * self.__tileDims["height"])
                else:            
                    offsetY = self.__tileDims["height"]
               
                
                if ((j + 1) == self.__tilesSize["columns"]):
                    offsetX = wlength - (j * self.__tileDims["width"])
                    offsetTextY = offsetY / 5
                else:
                    offsetX = self.__tileDims["width"]
                    offsetTextY = offsetY / 2
                    
                
                # Remember to invert the y-coordinate due the tkinter inverted viewport  (0,0 is at top window)    
                p1 = Point2D(j * self.__tileDims["width"], wheight -(i * self.__tileDims["height"]))
                p2 = Point2D(p1.x + offsetX, wheight - ((i * self.__tileDims["height"]) + offsetY))
                
                pp1 = viewport.W2V(p1)
                pp2 = viewport.W2V(p2)
                
                ret.append(canvas.create_rectangle(pp1.x, pp1.y, pp2.x, pp2.y, fill="gray", outline="brown"))
                
                tpos = Point2D(p1.x + (offsetX/2), wheight - ((i * self.__tileDims["height"]) + offsetTextY))
                ttpos = viewport.W2V(tpos)
                fontsize = int(300 / wlength)    # Using a magical number to fit the text size
                if (fontsize > 26):
                    fontsize = 26
                ret.append(canvas.create_text(ttpos.x, ttpos.y, text=str(self.__tiles[i][j].statusVal), font=('Arial', fontsize)))    
                
                j += 1
            i += 1

        
        
        return ret
    
    
    
    def DrawRubble(self, canvas, viewport):
        # Draw the rubble height lines
        
        ret = []
        
        wlength = self.__construction.GetLength()
        wheight = self.__construction.GetHeight()
        
        j = 0
        while (j < self.__tilesSize["columns"]):
            
            if ((j + 1) == self.__tilesSize["columns"]):
                offsetX = wlength - (j * self.__tileDims["width"])
            else:
                offsetX = self.__tileDims["width"]

            rh = wheight - self.__rubble[j]
            rp1 = Point2D(j * self.__tileDims["width"], rh)
            rp2 = Point2D(rp1.x + offsetX, rh)
            
            rrp1 = viewport.W2V(rp1)
            rrp2 = viewport.W2V(rp2)
           
            if (j in self.__gateways):
                color = "green"
            else:
                color = "Khaki"
            ret.append(canvas.create_line(rrp1.x, rrp1.y, rrp2.x, rrp2.y, fill=color, width = 4 ))
            
            j += 1
            
            
        return ret
    
    
    
    
    
    def HasGateways(self):
        return (len(self.__gateways) > 0)

        
    def GetDistanceClosestGateway(self, position, squared = False):
        # Returns the distance between given position and closest gateway. If squared is false returns the non-squared distance
        
        minD = -1
        
        for g in self.__gateways:
            
            c = self.GetTileCenter(self.__tiles[0][g])
            
            if (squared):
                d = c.Distance(position)
            else:
                d = ((c.x - position.x)**2) + ((c.y - position.y)**2) + ((c.z - position.z)**2)
                              
            if ((minD == -1) or (d < minD)):
                minD = d
            
        return minD
        
        
    def GetCloseGateway(self, position, searchrange):
        # Check if given position is close to a gateway, and return its index
        
        # Check for distances between gateway center (that is, a tile/column center) and given position
        
        minD = -1
        ret = None
        
        i = 0
        while (i < len(self.__gateways)):
            c = self.GetTileCenter(self.__tiles[0][self.__gateways[i]])
            d = position.Distance(c)
            if ((d <= searchrange) and ((d < minD) or not ret)):
                minD = d
                ret = i
            
            i += 1
            
        return ret
        
        
        
        
        """  --> Too much casuistic problems .... 
        # Project the four cell bounding vertices over each one of the gateway segments over the wall
        # The first projection that falls on any segment finish the method returning the index of related gateway

        
        seglist = self.GetGatewaySegmentList()
        if (not seglist):
            return None
        
        bound = cell.GetBoundingQuad()
        plist = bound.GetVertices()
        
        gateway = 0
        for seg in seglist:
            for p in plist:
                if (seg.ProjectPoint(point = p, forceprojection = True)):
                    return gateway
            
            gateway += 1
        """    
            
        return None
            
        
        
        
    def GetRandomGatewayPosition(self, gatewayindex, marginleft = 0.0, marginright = 0.0):
        # Return a random 2D position in front of given gateway
        # marginleft and marginright are used to limit the random positions on tile between given margins
        
        
        if ((gatewayindex < 0) or (gatewayindex >= len(self.__gateways))):
            return None 
        
        # Get the tile start position (take the ground tile)
        
        pos = self.__construction.GetStartPosition().Copy()
        pos.Move(self.__construction.GetWallVector(), self.__gateways[gatewayindex] * self.__tileDims["width"])
        
        
        # Get a random on the tile length
        l = self.__tileDims["width"] - marginright - marginleft
        #random.seed()
        r = marginleft + (random.random() * l)
        
        pos.Move(self.__construction.GetWallVector(), r)
        
        return pos
    
    
    
    
        

        
        
        
        
        
        