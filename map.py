from pygame import draw
import math
from pqueue import pqueue
from pqueue import stack

mapSize = (50,50)
blockSize = 8

startEnd = []
selection = []
solution = []
commands = stack()

def getSize():
    return (_forwardConversion(mapSize[0]-1)+blockSize+2, _forwardConversion(mapSize[1]-1)+blockSize+2)



def initialize(surface):
    global startEnd
    global selection
    global commands
    startEnd = []
    selection = []
    commands = stack()
    _resetSolution()
    _resetDraw(surface)

def _resetDraw(surface):
    surface.fill((0,0,0))
    for x in range(mapSize[0]):
        for y in range(mapSize[1]):
            _drawBlank(surface, x, y)


def _drawBlank(surface, x, y, reset = False):
    if reset:
        _drawAt(surface, x, y, (0,0,0), fill=True)
    _drawAt(surface, x, y, (25,25,25), 1)

def overlay(surface):
    global startEnd
    global selection
    for select in selection:
        _drawAt(surface, select[0], select[1], (125,125,125))
    if len(startEnd) > 0:
        _drawAt(surface, startEnd[0][0], startEnd[0][1], (0,255,0))
    if len(startEnd) > 1:
        _drawAt(surface, startEnd[1][0], startEnd[1][1], (255,0,0))

def _drawAt(surface, x, y, color, width = 0, fill = False):
    mod = 0
    if (fill):
        mod = 1
    draw.rect(surface, color, (_forwardConversion(x)-mod,_forwardConversion(y)-mod,blockSize+2*mod,blockSize+2*mod), width)

def _forwardConversion(p):
    return p*(blockSize+2)+1

def _backwardsConversion(p):
    return math.floor((p-1)/(blockSize+2))
    
def _pointToSquare(pos):
    x = _backwardsConversion(pos[0])
    y = _backwardsConversion(pos[1])
    return (x, y)

def select(pos):
    _pos = _pointToSquare(pos)
    x = _pos[0]
    y = _pos[1]
    if (x,y) in startEnd + selection:
        return
    commands.push((x,y))
    selection.append((x,y))

def undo(surface):
    last = commands.pop()
    if last is False:
        return
    if last in selection: selection.remove(last)
    if last in startEnd: startEnd.remove(last)
    _drawBlank(surface, last[0], last[1], True)


def selectEndpoint(pos):
    _pos = _pointToSquare(pos)
    x = _pos[0]
    y = _pos[1]
    if len(startEnd) > 1 or (x,y) in startEnd + selection:
        return
    commands.push((x,y))
    startEnd.append((x,y))

def solveReady():
    return len(startEnd) > 1

def hasSolved():
    if solvedPath is False:
        return False
    return len(solvedPath.previous) == 0



solution = []

queue = pqueue()
walked = []
newWalked = []

def _resetSolution():
    global solution
    global queue
    global walked
    global solvedPath
    global newWalked
    solution = []
    solvedPath = False
    queue = pqueue()
    walked = []
    newWalked = []


def stepSolution():
    global solvedPath
    global solution
    global queue
    global walked
    global newWalked
    if not solvedPath is False:
        if len(solvedPath.previous) > 0:
            solution.append(solvedPath.previous.pop(0))
            return True
        else:
            return False
    if len(walked) == 0:
        queue.enqueue(Path(False, startEnd[0][0], startEnd[0][1], 0))
        walked.append(startEnd[0])
    q = queue.dequeue()
    if q is False:
        return False
    # Check if currently on the end
    if (q.x, q.y) == startEnd[1]:
        solvedPath = q
        return True
    # Queue the surrounding blocks
    for x in range(-1, 2, 1):
        for y in range(-1, 2, 1):
            if q.x+x < 0 or q.y+y < 0 or q.x+x >= mapSize[0] or q.y+y >= mapSize[1]:
                continue
            if not (q.x + x, q.y + y) in walked:
                newWalked.append((q.x + x, q.y + y))
                walked.append((q.x + x, q.y + y))
                val = math.sqrt(abs(x) + abs(y))
                if (q.x+x, q.y+y) in selection:
                    val += 100
                queue.enqueue(Path(q, q.x+x, q.y+y, val))
                # Add walk value later
    
    return True
         #   for (int x = 1, y = 0; x+y != 0; y+=x, x-=y, y-=Convert.ToInt32(x == -1))


    
    

def drawSolution(surface):
    global newWalked
    if len(newWalked) > 0:
        for select in newWalked:
            _drawAt(surface, select[0], select[1], (200,200,0), width=1)
        newWalked = []
    else:
        for select in walked:
            _drawAt(surface, select[0], select[1], (200,200,0), width=1)
    if len(solution) > 0:
        for select in solution:
            _drawAt(surface, select[0], select[1], (255,255,255), fill=True)


class Path:
    def __init__(self, prev, x, y, val):
        self.value = val
        self.previous = []
        if not prev is False:
            self.value = prev.value + val
            self.previous = prev.previous.copy()
            self.previous.append((prev.x,prev.y))
        self.x = x
        self.y = y

    def compare(self, item):
        return self.value - item.value
