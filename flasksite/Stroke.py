from flask import current_app
#Represents approximate location of start/end points of stroke.
class Location:
    def __init__(self, x, y, display):
        self.x = x
        self.y = y
        self.display = display
    
    def toString(self):
        return display
    

    """
     * @param other Another direction
     * @return True if this direction is within one step of the other direction
    """
    @staticmethod
    def isClose(this, other):
        return abs(this.x - other.x) <= 1 and abs(this.y - other.y) <= 1
    
    """
     * @param x Normalised X
     * @param y Normalised Y
     * @return Location
    """
    @staticmethod
    def get(x, y):
        if(x < 85):
            if(y < 85):
                return Location.NW
            elif y < 170:
                return Location.W
            else:
                return Location.SW
        elif x < 170:
            if y < 85:
                return Location.N
            elif y < 170:
                return Location.MID
            else:
                return Location.S
        else:
            if y < 85:
                return Location.NE
            elif y < 170:
                return Location.E
            else:
                return Location.SE

# Basically N 
Location.N = Location(1, 0, "\u2580")
# Basically NE 
Location.NE = Location(2, 0, "\u259c")
# Basically E 
Location.E = Location(2, 1, "\u2590") 
# Basically SE 
Location.SE = Location(2, 2, "\u259f")
# Basically S 
Location.S = Location(1, 2, "\u2584") 
# Basically SW 
Location.SW = Location(0, 2, "\u2599") 
# Basically W 
Location.W = Location(0, 1, "\u258c")
# Basically NW 
Location.NW = Location(0, 0, "\u259b")
# Basically in the middle 
Location.MID = Location(1, 1, "\u2588")

###################################################################
class Direction:
        def __init__(self, index, display):
            self.index = index
            self.display = display

        def __str__(self):
            return "Direction(%s,%s)" % (self.index, self.display)

        def toString(self):
            return display
        
        """
         * @param other Another direction
         * @return True if this direction is within one step of the other direction
        """
        @staticmethod
        def isClose(this, other):
            if(this==Direction.X  or other==Direction.X  or this == other):
                return True
            return (this.index == ( (other.index + 1) % 8 ) ) or ( ((this.index + 1) % 8 ) == other.index)
        
        """
         * Calculates the direction between two points.
         * @param startX Start X
         * @param startY Start Y
         * @param endX End X
         * @param endY End Y
         * @return Direction of stroke
        """
        @staticmethod
        def get(startX, startY, endX, endY):
            # Get movement in each direction
            deltaX = endX - startX
            deltaY = endY - startY
            """
             * Propotion (out of 256) of dominant movement required to count as diagonal.
             * (E.g. if this is 77 = approx 30%, and if movement S is 10, then movenent E must
             * be at least 10 * 77 / 256 in order to count as SE).
             
            """
            DIAGONAL_THRESHOLD = 77
            # Threshold above which something counts as directional.
            DIRECTION_THRESHOLD = 51   #51*5=255
            
            #Check if it's not really movement at all (under threshold)
            absDeltaX = abs(deltaX)
            absDeltaY = abs(deltaY)
            if(absDeltaX < DIRECTION_THRESHOLD and absDeltaY < DIRECTION_THRESHOLD):
                return Direction.X
            
            if(absDeltaX > absDeltaY):
                # X movement is more significant
                diagonal = absDeltaY > ((DIAGONAL_THRESHOLD * absDeltaX) >> 8)    # dy/dx > 77/256
                if(deltaX > 0):
                    if(diagonal):
                        return Direction.NE if deltaY < 0 else Direction.SE
                    else:
                        return Direction.E
                else:
                    if(diagonal):
                        return Direction.NW if deltaY < 0 else Direction.SW
                    else:
                        return Direction.W
            else:
                #// Y movement is more significant
                diagonal = absDeltaX > ((DIAGONAL_THRESHOLD * absDeltaY) >> 8)
                if(deltaY > 0):
                    if(diagonal):
                        return Direction.SW if deltaX < 0 else Direction.SE
                    else:
                        return Direction.S
                else:
                    if(diagonal):
                        return Direction.NW if deltaX < 0 else Direction.NE
                    else:
                        return Direction.N
                    
# Basically N */
Direction.N = Direction(0, "N") 
# Basically NE */
Direction.NE = Direction(1, "NE") 
# Basically E */
Direction.E = Direction(2, "E") 
# Basically SE */
Direction.SE = Direction(3, "SE")
# Basically S */
Direction.S = Direction(4, "S") 
# Basically SW */
Direction.SW = Direction(5, "SW") 
# Basically W */
Direction.W = Direction(6, "W")
# Basically NW */
Direction.NW = Direction(7, "NW")
# No clear movement */
Direction.X = Direction(-1, "X")     


###################################################################
class Stroke(object):
    """docstring for Stroke"""
    def __init__(self, startX, startY, endX, endY):
        """
          @param startX Start position (x) 0-1
          @param startY Start position (y) 0-1
          @param endX End position (x) 0-1
          @param endY End position (y) 0-1
        """
        self.startX = self.convert(startX) 
        self.startY = self.convert(startY)
        self.endX = self.convert(endX)
        self.endY = self.convert(endY)

    def convert(self,v):
        #convert 0-1 to range 0-255
        return (int)(v * 255 + 0.49999)
    
    """ Calculates the direction of this stroke."""
    def getDirection(self):
        direction = Direction.get(self.startX, self.startY, self.endX, self.endY)
        current_app.logger.debug("startX=%s, startY=%s, endX=%s, endY=%s direction=%s", self.startX, self.startY, self.endX, self.endY,direction)
        return direction
    
    """
     * Calculates the direction that the pen moved between the end of the
     * last stroke and the start of this one.
     * @param previous Previous stroke
     * @return Direction moved
    """
    def getMoveDirection(self, previous):
        return Direction.get(previous.endX, previous.endY, self.startX, self.startY)
    
    """
     * @return Approximate location of start of stroke
    """
    def getStartLocation(self):
        return Location.get(self.startX, self.startY)
    
    """
     * @return Approximate location of end of stroke
    """
    def getEndLocation(self):
        return Location.get(self.endX, self.endY)
    
    def toString(self):
        return "[" + self.startX + "," + self.startY + ":" + self.endX + "," + self.endY + "]"
