class QuadTreeItem:

    def __init__(self,left=0,top=0,right=0,bottom=0):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def startQTBoundaries(self,x,y,w,h):
        self.left = x
        self.top = y
        self.right = x+w
        self.bottom = y+h