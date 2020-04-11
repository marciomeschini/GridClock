import unicornhathd
import time
from datetime import datetime
from pytz import timezone

class Size:
    def __init__(self, width, height):
        self.width = int(width)
        self.height = int(height)
        
    def __repr__(self):
        return "{width:%s, height:%s}" % (self.width, self.height)

class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        
    def __repr__(self):
        return "{x:%s, y:%s}" % (self.x, self.y)

class Color:    
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        
    def __repr__(self):
        return "{r:%s, g:%s, b:%s}" % (self.r, self.g, self.b)
        
    @staticmethod
    def black():
        return Color(0, 0, 0)
    
    @staticmethod
    def white():
        return Color(255, 255, 255)

class Pixel:
    def __init__(self, point, color):
        self.point = point
        self.color = color
        
    def __repr__(self):
        return "{point:%s, color:%s}" % (self.point, self.color)

class Grid:
    def __init__(self, size, pixels):
        self.size = size
        self.pixels = pixels
        
    def __repr__(self):
        return "{size:%s, pixels:%s}" % (self.size, self.pixels)
        
    @classmethod
    def toIndex(cls, point, size):
        return int(point.y * size.width + point.x)
        
    @classmethod
    def toPoint(cls, index, size):
        return Point(index % size.width, index / size.width)
        
    @classmethod
    def same(cls, size, color):
        count = size.width * size.height
        pixels = []
        for index in range(count):
            point = Grid.toPoint(index, size)
            pixel = Pixel(point, color)
            pixels.append(pixel)
        return Grid(size, pixels)
       
    @classmethod
    def number(cls, size, number):
        pixels = []
        for offset, element in enumerate(number):
            point = Grid.toPoint(offset, size)
            pixel = Pixel(point, Color.white() if element > 0 else Color.black())
            pixels.append(pixel)
        return Grid(size, pixels)
    
    def appending(self, grid, point):
        mutable=self.pixels
        for offset, element in enumerate(grid.pixels):
            # swap X with Y. Not sure if related to rotation.
            dest = Point(element.point.y + point.y, element.point.x + point.x)
            index = Grid.toIndex(dest, self.size)
            mutable[index] = Pixel(dest, element.color)
        return Grid(self.size, mutable)


class ThreeByFive:
    def __init__(self):
        self.size = Size(3, 5)
        self.values = [
            [1, 1, 1,  1, 0, 1,  1, 0, 1,  1, 0, 1,  1, 1, 1],
            [0, 0, 1,  0, 1, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1],
            [1, 1, 1,  0, 0, 1,  1, 1, 1,  1, 0, 0,  1, 1, 1],
            [1, 1, 1,  0, 0, 1,  1, 1, 1,  0, 0, 1,  1, 1, 1],
            [1, 0, 1,  1, 0, 1,  1, 1, 1,  0, 0, 1,  0, 0, 1],
            [1, 1, 1,  1, 0, 0,  1, 1, 1,  0, 0, 1,  1, 1, 1],
            [1, 1, 1,  1, 0, 0,  1, 1, 1,  1, 0, 1,  1, 1, 1],
            [1, 1, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1],
            [1, 1, 1,  1, 0, 1,  1, 1, 1,  1, 0, 1,  1, 1, 1],
            [1, 1, 1,  1, 0, 1,  1, 1, 1,  0, 0, 1,  0, 0, 1],
        ]
        
class ThreeBySeven:
    def __init__(self):
        self.size = Size(3, 7)
        self.values = [
            [1, 1, 1,  1, 0, 1,  1, 0, 1,  1, 0, 1,  1, 0, 1,  1, 0, 1,  1, 1, 1],
            [0, 0, 1,  0, 1, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1],
            [1, 1, 1,  0, 0, 1,  0, 0, 1,  1, 1, 1,  1, 0, 0,  1, 0, 0,  1, 1, 1],
            [1, 1, 1,  0, 0, 1,  0, 0, 1,  1, 1, 1,  0, 0, 1,  0, 0, 1,  1, 1, 1],
            [1, 0, 1,  1, 0, 1,  1, 0, 1,  1, 1, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1],
            [1, 1, 1,  1, 0, 0,  1, 0, 0,  1, 1, 1,  0, 0, 1,  0, 0, 1,  1, 1, 1],
            [1, 1, 1,  1, 0, 0,  1, 0, 0,  1, 1, 1,  1, 0, 1,  1, 0, 1,  1, 1, 1],
            [1, 1, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1],
            [1, 1, 1,  1, 0, 1,  1, 0, 1,  1, 1, 1,  1, 0, 1,  1, 0, 1,  1, 1, 1],
            [1, 1, 1,  1, 0, 1,  1, 0, 1,  1, 1, 1,  0, 0, 1,  0, 0, 1,  0, 0, 1],
        ]

def make_grid(source, generator, value):
    columns = 4
    accumulator = source
    size = generator.size
    for offset, element in enumerate(value):
        x = (offset%columns)*(size.width+1)
        y = int(offset/columns)*(size.height+1)
        child = Grid.number(size, generator.values[int(element)])
        accumulator = accumulator.appending(child, Point(x, y))
    return accumulator

def tick(source, generator):
    utc_time = datetime.now(timezone('UTC'))
    local_timezone = timezone('Europe/London')
    formatted = utc_time.astimezone(local_timezone).strftime("%H%M%S")
    currentGrid = make_grid(source, generator, formatted)
    for e in currentGrid.pixels:
        unicornhathd.set_pixel(e.point.x, e.point.y, e.color.r, e.color.g, e.color.b)
    unicornhathd.show()

master = Grid.same(Size(16, 16), Color.black())
#generator = ThreeByFive()
generator = ThreeBySeven()

unicornhathd.brightness(0.75)

try:
    while True:
        tick(master, generator)
        time.sleep(1)
        
except KeyboardInterrupt:
    unicornhathd.off()
    exit(0)
