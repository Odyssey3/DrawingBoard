from graphics import *
from math import *
class Sprite:
    def __init__(self, *args):
        self.drawings = []
        for arg in args:
            self.drawings.append(arg)

    def add(self, *args):
        for arg in args:
            self.drawings.append(arg)
    def draw(self):
        for d in self.drawings:
            d.draw()
    def undraw(self):
        for d in self.drawings:
            d.undraw()
    def move(self, dx, dy):
        for d in self.drawings:
            d.move(dx, dy)
    def rotate(self, angle, centerX = None, centerY = None, direction = True):
        x0, y0, x1, y1 = self.getRect()
        if centerX == None:
            centerX = (x1+x0)/2
        if centerY == None:
            centerY = (y1+y0)/2
        for d in self.drawings:
            d.rotate(angle, centerX, centerY, direction)

    def getRect(self):
        x0, y0, x1, y1 = self.drawings[0].getRect()
        for d in self.drawings:
            x0_, y0_, x1_, y1_ = d.getRect()
            x0 = min(x0, x0_)
            x1 = max(x1, x1_)
            y0 = min(y0, y0_)
            y1 = max(y1, y1_)
        return x0, y0, x1, y1
class drawingObject:
    def __init__(self, obj, board, type = "figure", width = 0):
        self.board = board;
        self.obj = obj
        self.width = width
        self.type = type
        self.visibility = False
        self.points = []
        if type == "point":
            x, y = obj.p1.getX() + width, obj.p1.getY() + width
            self.points.append(Point(x, y))
            # self.point1 = Point(x, y)
            # self.point2 = Point(x, y)
        elif type == "text":
            x, y = obj.anchor.getX(), obj.anchor.getY()
            self.points.append(Point(x, y))

            # self.point1 = Point(x, y)
            # self.point2 = Point(x, y)
        elif type == 'polygon':
            for pnt in obj.points:
                x, y = pnt.getX(), pnt.getY()
                self.points.append(Point(x, y))
            # self.point1 = Point(x, y)
            # self.point2 = Point(x, y)
        else:
            self.points.append(obj.p1)
            self.points.append(obj.p2)
            # self.point1 = obj.p1
            # self.point2 = obj.p2

    def draw(self):
        if self.visibility:
            return
        x, y = self.board.convert(self.points[0].getX(),self.points[0].getY())
        if self.type == "point":
            self.obj.p1 = Point(x-self.width, y-self.width)
            self.obj.p2 = Point(x+self.width, y+self.width)
        elif self.type == "text":
            self.obj.anchor = Point(x, y)
        elif self.type == "polygon":
            self.obj.points.clear()
            for pnt in self.points:
                x, y = self.board.convert(pnt.getX(), pnt.getY())
                self.obj.points.append(Point(x, y))
        else:
            self.obj.p1 = Point(x, y)
            x, y = self.board.convert(self.points[1].getX(), self.points[1].getY())
            self.obj.p2 = Point(x, y)
        self.obj.draw(self.board.board)
        self.visibility = True

    def undraw(self):
        self.obj.undraw()
        self.visibility = False

    def move(self,dx,dy):
        i = 0
        for pnt in self.points:
            x, y = pnt.getX(), pnt.getY()
            pnt = Point(x + dx, y + dy)
            self.points[i] = pnt
            i = i + 1
        # x, y = self.point1.getX(), self.point1.getY()
        # self.point1 = Point(x+dx, y+dy)
        # x, y = self.point2.getX(), self.point2.getY()
        # self.point2 = Point(x+dx, y+dy)
        if self.visibility:
            self.undraw()
            self.draw()
    def rotate(self,  angle, centerX = None, centerY = None, direction = True):
        # pnt = Point(x + dx, y + dy)
        # x, y = self.point1.getX(), self.point1.getY()
        # x1, y1 = self.point2.getX(), self.point2.getY()
        x, y, x1, y1 = self.getRect()
        if centerX == None:
            centerX = (x1+x)/2
        if centerY == None:
            centerY = (y1+y)/2

        if direction:
            sign = -1
        else:
            sign = 1

        i = 0
        if self.type == 'circle':
            pnt1 = self.points[0]
            pnt2 = self.points[1]
            x1, y1 = pnt1.getX(), pnt1.getY()
            x2, y2 = pnt2.getX(), pnt2.getY()

            radiusX = max((x2-x1),(x1-x2))/2
            radiusY = max((y2-y1),(y1-y2))/2
            x, y = (x2+x1)/2, (y2+y1)/2

            x, y = x - centerX, y - centerY
            newX = x * cos(angle) - sign * y * sin(angle)
            newY = sign * x * sin(angle) + y * cos(angle)
            x, y = newX + centerX, newY + centerY

            x1, y1 = x-radiusX, y-radiusY
            x2, y2 = x+radiusX, y+radiusY

            pnt1 = Point(x1, y1)
            self.points[0] = pnt1

            pnt2 = Point(x2, y2)
            self.points[1] = pnt2

        else:
            for pnt in self.points:
                x, y = pnt.getX(), pnt.getY()
                x, y = x-centerX, y-centerY
                newX = x*cos(angle) - sign*y*sin(angle)
                newY = sign*x*sin(angle) + y*cos(angle)
                x, y = newX+centerX, newY+centerY
                pnt = Point(x, y)
                self.points[i] = pnt
                i = i + 1
        if self.visibility:
            self.undraw()
            self.draw()

    def moveTo(self,x,y, x1 = None, y1 = None ):

        if x1 == None:
            newX1 = x + self.point2.getX() - self.point1.getX()
        else:
            newX1 = x1
        if y1 == None:
            newY1 = y + self.point2.getY() - self.point1.getY()
        else:
            newY1 = y1
        self.point1 = Point(x, y)
        self.point2 = Point(newX1, newY1)
        if self.visibility:
            self.undraw()
            self.draw()

    def getRect(self):
        xmin = min(list(map(lambda pnt: pnt.getX(), self.points)))
        xmax = max(list(map(lambda pnt: pnt.getX(), self.points)))
        ymin = min(list(map(lambda pnt: pnt.getY(), self.points)))
        ymax = max(list(map(lambda pnt: pnt.getY(), self.points)))
        return xmin, ymin, xmax, ymax

class drawingBoard:
    def __init__(self, size_x=0, size_y=0, scale=1, background_color='white', pen_color='red', name = 'Drawing board'):
        self.size_x = size_x
        self.size_y = size_y
        self.scale_x = scale
        self.scale_y = scale
        self.range_x = size_x*scale
        self.range_y = size_y*scale
        self.pen_color = pen_color
        self.background_color = background_color
        self.orientacion_x = True
        self.orientacion_y = True
        self.setOrigin('center')
        self.objects = []
        self.gridLines = []
        self.name = name
        self.board = GraphWin(name, size_x, size_y)
        self.grid = False
        self.axis = False
        self.step_x = 1
        self.step_y = 1
        self.grid_color = self.pen_color
        self.grid_text = False
    def setOrigin(self, origin_position="free", origin_x=0, origin_y=0):
        self.origin_position = origin_position
        if origin_position == 'center':
            self.origin_x = self.size_x // 2
            self.origin_y = self.size_y // 2
        elif origin_position == 'left_top':
            self.origin_x = 0
            self.origin_y = self.size_y
        elif origin_position == 'left_bottom':
            self.origin_x = 0
            self.origin_y = 0
        elif origin_position == 'left_center':
            self.origin_x = 0
            self.origin_y = self.size_y // 2
        elif origin_position == 'right_center':
            self.origin_x = self.size_x
            self.origin_y = self.size_y // 2
        elif origin_position == 'right_bottom':
            self.origin_x = self.size_x
            self.origin_y = 0
        elif origin_position == 'right_top':
            self.origin_x = self.size_x
            self.origin_y = self.size_y
        else:
            self.origin_x = origin_x
            self.origin_y = origin_y
    def setSize(self, size_x=0, size_y=0, rerange = True):
        self.size_x = size_x
        self.size_y = size_y
        if rerange:
            self.range_x = size_x*self.scale_x
            self.range_y = size_y*self.scale_y
        else:
            self.scale_x = self.size_x/range_x
            self.scale_y = self.size_y/range_y

        self.board.close()
        self.board = GraphWin(self.name, size_x, size_y)
        self.update()
    def setScale(self, scale_x=1, scale_y=None):
        if scale_y == None:
            scale_y = scale_x
        if scale_x<=0:
            scale_x = 1
        if scale_y<=0:
            scale_y = 1
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.range_x = self.size_x/scale_x
        self.range_y = self.size_y/scale_y
        self.update()
    def setRange(self, range_x=1, range_y=None, resize=True):
        if range_y == None:
            range_y = range_x
        if range_x<=0:
            range_y = 1
        if range_y<=0:
            range_y = 1
        self.range_x = range_x
        self.range_y = range_y
        if resize:
            size_x = self.scale_x * range_x
            size_y = self.scale_y * range_y
            self.setSize(size_x, size_y)
        else:
            scale_x = self.size_x/range_x
            scale_y = self.size_y/range_y
            self.setScale(scale_x, scale_y)
        # self.update()
    def setBorders(self,x, y, x1, y1, resize = True):
        self.setRange(x1-x, y1-y,resize)
        self.setOrigin("free", (0-x)*self.scale_x,(0-y)*self.scale_y)
        self.update()
    def setColors(self, background_color='white', pen_color='black'):
        self.pen_color = pen_color
        self.background_color = background_color
    def setOrientahion(self, orientacion_x, orientacion_y):
        self.orientacion_x = orientacion_x
        self.orientacion_y = orientacion_y
    def getMouse(self):
        self.board.getMouse()
    def convert(self, x, y):
        x = x * self.scale_x
        x = x + self.origin_x
        if not self.orientacion_x: x = self.size_x - x
        y = y * self.scale_y
        y = y + self.origin_y
        if self.orientacion_y: y = self.size_y - y
        return x,y
    def point(self, x=0, y=0, width = 1, color = None, visibility = True):
        if color==None:
            color = self.pen_color
        # x, y = self.convert(x, y)
        c = Circle(Point(x, y), width)
        c.setWidth(1)
        c.setFill(color)
        c.setOutline(color)
        obj = drawingObject(c, self, type = "point", width = width)
        if visibility:
            obj.draw()
        self.objects.append(obj)
        return obj
    def text(self, x=0, y=0, msg = "", size = 8, color = None, style = None, grid = False, visibility=True):
        if color==None:
            color = self.pen_color
        if style==None:
            style = ""

        t = Text(Point(x,y), msg)
        t.setTextColor(color)
        t.setSize(size)
        obj = drawingObject(t, self, type = 'text')
        if visibility:
            obj.draw()
        if grid:
            self.gridLines.append(obj)
        else:
            self.objects.append(obj)
        return obj
    def circle(self, x=0, y=0, radius=1, width=1, color=None, fill=None, visibility=True):
        if color == None:
            color = self.pen_color
        if fill == None:
            fill = self.background_color
        x = x-radius
        y = y-radius
        x1 = x+radius
        y1 = y+radius
        c = Oval(Point(x, y), Point(x1,y1))
        c.setWidth(width)
        c.setFill(fill)
        c.setOutline(color)
        obj = drawingObject(c, self, type = 'circle')
        if visibility:
            obj.draw()
        self.objects.append(obj)
        return obj
    def line(self, x, y, x1, y1, width=1, color=None, grid = False, visibility = True):
        if color == None:
            color = self.pen_color
        # x, y = self.convert(x, y)
        # x1, y1 = self.convert(x1, y1)
        l = Line(Point(x, y), Point(x1, y1))
        l.setFill(color)
        l.setWidth(width)
        obj = drawingObject(l, self)
        if visibility:
            obj.draw()

        if grid:
            self.gridLines.append(obj)
        else:
            self.objects.append(obj)
        return obj
    def rect(self, x, y, x1, y1, width=1, color=None, visibility = True):
        if color == None:
            color = self.pen_color
        # x, y = self.convert(x, y)
        # x1, y1 = self.convert(x1, y1)
        r = Rectangle(Point(x, y), Point(x1, y1))
        r.setFill(color)
        r.setWidth(width)
        obj = drawingObject(r, self)
        if visibility:
            obj.draw()
        self.objects.append(obj)
        return obj
    def polygon(self, *points, width=1, color=None, visibility=True,  fill=None):
        if color == None:
            color = self.pen_color
        # x, y = self.convert(x, y)
        # x1, y1 = self.convert(x1, y1)
        # vertices = [points[0],points[1],points[2]]
        # triangle = Polygon(vertices)
        # triangle.setFill('gray')
        # triangle.setOutline('cyan')
        # triangle.setWidth(4)  # width of boundary line
        # obj = triangle.draw(self.board)
        p = Polygon(list(points))
        p.setFill(color)
        p.setWidth(width)
        obj = drawingObject(p, self, type = 'polygon')
        if visibility:
            obj.draw()
        self.objects.append(obj)
        return obj
    def clear(self, fast = False):
        self.board.autoflush = False
        for item in self.board.items[:]:
            item.undraw()
        self.board.items.clear()
        if self.grid:
            self.drawGrid()
        self.board.autoflush = False
        self.board.redraw()
        # return
        # if not fast:
        #     for obj in self.objects:
        #         obj.undraw()
        #         self.objects.clear()
        # else:
        #     self.objects.clear()
        #     x0, y0, x1, y1 = self.getScreenCoords()
        #     self.board.close()
        #     self.board = GraphWin(self.name, self.size_x, self.size_y)
        #     self.moveBoardTo(x0, y0)
        #     self.update()
    def undo(self):
        obj = self.objects.pop()
        obj.undraw()
    def update(self):
        if self.origin_position == 'free':
            self.setOrigin(origin_x=self.origin_x, origin_y=self.origin_y)
        else:
            self.setOrigin(origin_position=self.origin_position)

        for obj in self.objects:
            if obj.visibility:
                obj.undraw()
                obj.draw()
        if self.grid:
            self.undrawGrid()
            self.drawGrid()
    def resizeToX(self):
        self.setScale(self.scale_x)
    def resizeToY(self):
        self.setScale(self.scale_y, self.scale_y)
    def drawGrid(self, step_x = None, step_y = None, width = 1, color = None, grid_text = None, text_size = 8):
        self.grid = True
        if grid_text == None:
            grid_text = self.grid_text
        self.grid_text = grid_text

        if step_x==None:
            step_x = self.step_x
        else:
            self.step_x = step_x
            if step_y == None:
                step_y = step_x
        if step_y == None:
            step_y = self.step_y
        else:
            self.step_y = step_y
        if color == None:
            color = self.grid_color

        self.grid_color = color
        center_x = self.origin_x/self.scale_x
        center_y = self.origin_y/self.scale_y
        left_x = 0 - center_x
        right_x = self.range_x - center_x
        top_y = 0 - center_y
        bottom_y = self.range_y - center_y

        znak = 0
        if not left_x==0:
            znak = left_x/abs(left_x)

        min_x = znak*(znak*left_x//step_x)*step_x
        max_x = (right_x//step_x)*step_x
        min_y = (top_y//step_y)*step_y
        max_y = (bottom_y//step_y)*step_y
        x = min_x
        # ysize = max(len(str(max_y)),len(str(min_y)))/2

        while x<=max_x:
            # tsize = len(str(x))/2
            xsize = text_size * (len(str(x)) / 2) / self.scale_x
            ysize = text_size/self.scale_y
            kf = 1
            if x==0: kf = 2
            self.line(x,bottom_y,x,top_y, width=width*kf, color=self.grid_color, grid=True)
            if self.grid_text:
                if (x+xsize) > right_x:
                    tx = right_x - xsize
                elif(x-xsize) < left_x:
                    tx = left_x + xsize
                else:
                    tx = x
                self.text(tx,top_y+ysize,""+str(x), grid=True, size=text_size)
                self.text(tx,bottom_y-ysize, ""+str(x), grid=True, size=text_size)
            x = x+step_x
        y = min_y
        while y<=max_y:
            xsize = text_size*(len(str(y)) / 2)/self.scale_x
            ysize = text_size/self.scale_y
            kf = 1
            if y==0: kf = 2
            self.line(left_x,y,right_x,y, width=width*kf, color=self.grid_color, grid=True)
            if self.grid_text:
                if (y+ysize) > bottom_y:
                    ty = top_y - ysize
                elif(y-ysize) < top_y:
                    ty = bottom_y + ysize
                else:
                    ty = y
                self.text(left_x + xsize,ty,""+str(y), grid=True, size=text_size)
                self.text(right_x - xsize,ty, ""+str(y), grid=True, size=text_size)
            y = y+step_y
    def undrawGrid(self):
        for obj in self.gridLines:
            obj.undraw()
        self.gridLines.clear()
        self.grid = False
    def redrawGrid(self):
        for obj in self.gridLines:
            obj.draw()
    def getScreenCoords(self):
        leftX = self.board.master.winfo_x()
        rightX = leftX+self.board.master.winfo_width()
        topY = self.board.master.winfo_y()
        bottomY = topY+self.board.master.winfo_height()
        return leftX, topY, rightX, bottomY
    def getBestStep(self):
        return self.range_x/self.size_x, self.range_y/self.size_y
    def moveBoardTo(self, newX, newY):
        self.board.master.geometry('%dx%d+%d+%d' % (self.size_x, self.size_y, newX, newY))
if __name__ == "__main__":

    DB = drawingBoard(500, 500)
    DB.setOrigin("center")
    # DB.setRange(100,6,False)
    # p1 = DB.point(0,0,3)
    # p2 = DB.point(0,3,3,'green')
    # l = DB.line(0, 0, 40, 40)
    # r = DB.rect(0, 0, 40, 40, color='green')
    # spr = Sprite()
    # spr.add(r, c1, c2)
    # spr.draw()
    # DB.getMouse()
    # for i in range(1,100):
    #     spr.move(1,0)
    # DB.getMouse()
    # for i in range(1,10):
    #     l.rotate(pi/6, 0, 0)
    #     DB.getMouse()
    p01 = Point(0,0)
    p02 = Point(0, 40)
    p03 = Point(40,40)
    p04 = Point(40,0)
    plg = DB.polygon(p01,p02,p03, p04, color='green')

    c1 = DB.circle(15,35,7)
    c2 = DB.circle(30,35,7)

    spr = Sprite()
    spr.add(plg, c1, c2)
    spr.draw()
    # DB.getMouse()

    crc = DB.circle(100,100,20)
    ln  = DB.line(100,100,80,80)
    DB.getMouse()
    crc.rotate(pi/6,0,0)
    ln.rotate(pi/6,0,0)
    DB.getMouse()
    ln.rotate(pi/6,0,0)
    crc.rotate(pi/6,0,0)
    DB.getMouse()
    ln.rotate(pi/6,0,0)
    crc.rotate(pi/6,0,0)
    DB.getMouse()
    ln.rotate(pi/6,0,0)
    crc.rotate(pi/6,0,0)
    DB.getMouse()
    ln.rotate(pi/6,0,0)
    crc.rotate(pi/6,0,0)
    DB.getMouse()
    ln.rotate(pi/6,0,0)
    crc.rotate(pi/6,0,0)
    DB.getMouse()

    # for i in range(1,10):
    #     spr.rotate(pi/6)
    #     DB.getMouse()



    # plg.draw(DB.board)
    # DB.getMouse()
    # for i in range(1,10):
    #     plg.rotate(pi/6)
    #     DB.getMouse()
    # DB.getMouse()
    # DB.drawGrid(2, 1, color='green', grid_text=True)
    # DB.getMouse()
    # DB.setBorders(-1, -1, 4, 4, False)
    # DB.getMouse()
    # DB.clear(fast=False)
    # DB.getMouse()
    # # for i in range(1,10):
    # #     # DB.setBorders(-1+i, -1, 4+i, 4, False)
    # #     # p2.moveTo(i*0.1,1)
    # #     l1.move(0.1,0)
    # #     DB.getMouse()
