#Advent Of Code 2024 day 6 
#by dfrodrig-git 

import re
import logging
import sys
import time
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

testRun = False

def assertExpected( result, expected,part=1):
    logger.info(f'Result part:{part}: {result}, expected: {expected}')
    if result != expected and testRun :
        logger.critical("Unnaceptable!")
    

def getInput(day = 6) :
    if testRun :
        f=open(f'inputDay{day}Test.txt')
    else :
        f=open(f'inputDay{day}.txt')
    
    return [line.strip() for line in f]

        
vector = {
    'N' : [(0,1), 'E'],
    'E' : [(1,0), 'S'],
    'S' : [(0,-1), 'W'],
    'W' : [(-1,0), 'N'],
    }

    
    
class Node() :
    def __init__(self, x, y, isObstacle = False) :
        self.x = x
        self.y = y
        self.pos = (x,y)
        self.visited = False
        self.isObstacle = isObstacle
    
    def getNextPosition(self, direction) :
        return (self.x + vector[direction][0][0], self.y + vector[direction][0][1])
    
    def getPreviousPosition(self, direction):
        return (self.x - vector[direction][0][0], self.y - vector[direction][0][1])
    
    def __str__(self) :
        return f'Node: {self.pos}, [{self.visited}, {self.isObstacle}]'
    def __repr__(self) :
        return f'Node: {self.pos}, [{self.visited}, {self.isObstacle}]'

class Path() :
    def __init__(self, startNode, worldMap, startDirection='N', newBlocker = None, visitedNodes=None) :
        self.startNode = startNode
        self.startDirection = startDirection
        self.visitedNodes = [] if not visitedNodes else visitedNodes
        self.worldMap = worldMap
        self.newBlocker = newBlocker if newBlocker is not startNode else None
    
    def getPotentialBlockers(self) :
        blockers = [(self.getNextNode(x,y),step) for x,y,step in self.visitedNodes]
        
        
        return [(node, direction, step) for ((node, result, direction),step) in blockers if result ==1]
    
    
    def getVisitedNodes(self) :
        return set([x for x, y, step in self.visitedNodes])
    
    def getNextNode(self, curNode, direction) :
        #print(f"[DEBUG] curNode:{curNode}, direction:{direction}")
        nextNode = self.worldMap.getNode(curNode.getNextPosition(direction))
        if not nextNode:
            return None, -1, "Out of Boundaries"
        
        if nextNode.isObstacle or nextNode == self.newBlocker :
            return self.getNextNode(curNode, vector[direction][1])
        
        return nextNode, 1, direction
    
    def buildPath(self) :
        curNode = self.startNode
        direction = self.startDirection 
        
        step = 0
        while curNode :
            curNode.visited = True
            self.visitedNodes.append((curNode, direction, step))
            step +=1
            
            curNode, result, direction = self.getNextNode(curNode, direction)
            if result == -1 :
                return "out :(", curNode, direction
            if (curNode, direction) in [(x,y) for x,y,z in self.visitedNodes] :
                return "blocked", curNode, direction


class WorldMap() :
    def __init__(self, data=None) :
        self.worldMap = {}
        self.startNode = None
        self.buildMap(data) if data else None

    
    def buildMap(self, dataInput) :
        self.MAX_ROWS = len(dataInput)-1
        self.MAX_COLS = len(dataInput[0])-1
        
        for y, line in enumerate(dataInput) :
            yflip = self.MAX_ROWS-y
            for x, value in enumerate(line) :
                self.worldMap[(x,yflip)] = Node(x,yflip, True if value == "#" else False)
                if value == "^" :
                    self.startNode = self.worldMap[(x,yflip)]
    
    def getNode(self, pos) :
        return self.worldMap.get(pos, None)
    
    def getVisited(self) :
        return [x for x in self.worldMap.values() if x.visited]
    
    '''
    deprecated
    python does not like recursive, uses too to many stack frames, no optimization :( )
    '''
    def walkMap(self, curNode, direction) :
        curNode.visited = True
        
        nextNode = worldMap.getNode(curNode.getNextPosition(direction))
        if not nextNode :
            return "Out of Boundaries"
        
        if nextNode.isObstacle :
            return self.walkMap(curNode, vector[direction][1])            
        
        return self.walkMap(nextNode, direction)
        
    
data = getInput()
worldMap = WorldMap(data)
originalPath = Path(worldMap.startNode, worldMap)
originalPath.buildPath()
print(f"Original: {originalPath.startNode}")
assertExpected(len(originalPath.getVisitedNodes()), 41)

#part 2
print(f"Part2")
print(originalPath.getPotentialBlockers())
result = []

begin = time.time()
timeElapsed = 0
stepTime=begin
for blocker in originalPath.getPotentialBlockers() :
    blockNode, blockDirection, step = blocker
    divergePos = blockNode.getPreviousPosition(blockDirection)
    print(f"Current blocker: {blockNode}, {blockDirection}, divergePos: {divergePos}, currentStep: {step}")
    print(f"timeElapsed: {time.time()-stepTime:.2f}s sinceBegin:{stepTime-begin:.2f}") 
    stepTime = time.time() 
    newPath = Path(worldMap.getNode(divergePos), 
                   worldMap, 
                   startDirection=blockDirection,
                   newBlocker = blockNode, 
                   visitedNodes = [x for x in originalPath.visitedNodes if step < step ])

    outcome, node, direction = newPath.buildPath()
    if outcome == "blocked":
        result.append((node, direction))

#2192 high; 2158 high; 531 low; wrong:1937; 2049 wrong.
assertExpected(len(result), 6, part=2)
        
