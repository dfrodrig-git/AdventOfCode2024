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
    def __init__(self, x, y) :
        self.x = x
        self.y = y
        self.pos = (x,y)
    
    def getNextPosition(self, direction) :
        return (self.x + vector[direction][0][0], self.y + vector[direction][0][1])
    
    def getPreviousPosition(self, direction):
        return (self.x - vector[direction][0][0], self.y - vector[direction][0][1])
    
    def __str__(self) :
        return f'Node: {self.pos}'#', [{self.visited},]'#'#{self.isObstacle}]'
    def __repr__(self) :
        return f'Node: {self.pos}'#', [{self.visited},]'#' {self.isObstacle}]'    



class PathNode(Node) :
    def __init__(self, node, direction, index, previousNode=None, nextNode=None) :
        #print(f'Creating PathNode: {node}, {direction}, {type(node)}')
        super().__init__(node.x, node.y)
        self.node = node
        self.direction = direction
        self.previous = previousNode
        self.next = nextNode
        self.index = index

class Path(): 
    def __init__(self, startPathNode) :
        self.startPathNode = startPathNode
        self.pathNodes = {(startPathNode.node, startPathNode.direction):startPathNode}
        self.looping = False
        self.outOfBounds = False
   
     
    def appendNode(self, node, direction, previousPathNode) :
        
        if node is None :
            self.setOutOfBounds() 
            return 'outOfBounds detected'

        if (node, direction) in self.pathNodes:
            self.setLooping() 
            return self.pathNodes.get((node, direction))
        
        pathNode = PathNode(node, direction, previousPathNode.index)
        self.pathNodes[(pathNode.node, pathNode.direction)] = pathNode
        return pathNode
    
    def setLooping(self) :
        self.looping = True
    
    def setOutOfBounds(self) :
        self.outOfBounds = True

class PathBuilder() :
    def __init__(self, startPathNode, worldMap, addObstacle = []) :
        self.worldMap = worldMap
        self.startPathNode = startPathNode
        #self.addObstacle = addObstacle
        
        
    def buildPath(self, addObstacle = []) :
        path = Path(self.startPathNode)
        #print(f"Creating New Path on WorldMap, with an obstacle {addObstacle}  ")
        curPathNode = path.startPathNode
        
        while curPathNode :
            nextNode, direction = self.worldMap.getNextNode(curPathNode.node, 
                                                          curPathNode.direction, 
                                                          addObstacle)
            if nextNode == None:
                    path.setOutOfBounds()
                    return path
            
            nextPathNode = path.appendNode(nextNode, direction, curPathNode)
            
            if path.looping :
                return path

            #print(f'Got next Node: {nextPathNode}')
            curPathNode = nextPathNode 
  
        print(f"Error: Should never get here: {curPathNode}")
        return "Error: should never get here"



class WorldMap() :
    def __init__(self, data=None) :
        self.worldMap = {}
        self.startNode = None
        self.obstacles = []
        self.buildMap(data) if data else None
        self.allNodes = set(self.worldMap.values())

    
    def buildMap(self, dataInput) :
        self.MAX_ROWS = len(dataInput)-1
        self.MAX_COLS = len(dataInput[0])-1
        
        for y, line in enumerate(dataInput) :
            yflip = self.MAX_ROWS-y
            for x, value in enumerate(line) :
                node = Node(x,yflip)
                self.worldMap[(x,yflip)] = node 
                self.startNode = node if value == "^" else self.startNode
                self.obstacles.append(node) if value == "#" else None 
                    
    def getStartNode(self) :
        return PathNode(self.startNode, "N", 0 )
    
    def getNode(self, pos) :
        return self.worldMap.get(pos, None)
    
    def getNextNode(self, node, direction, addObstacles=[]) :
        #print(f'[DEBUG]  Getting next node: {node}, {direction}')
        nextNode = self.getNode(node.getNextPosition(direction)) if node else None 
        
        if not nextNode :
            return None, None #Out Of Bounds
        
        if nextNode in self.obstacles or nextNode in addObstacles :
            return self.getNextNode(node, vector[direction][1], addObstacles)
        
        return nextNode, direction
        

#part 1
data = getInput()
worldMap = WorldMap(data)
pathBuilder = PathBuilder(worldMap.getStartNode(), worldMap)
path = pathBuilder.buildPath()
assertExpected(len(set([pathNode.node for pathNode in path.pathNodes.values() ])), 41)

#part 2
loopingPaths = []
obstacles = set([x.node for x in path.pathNodes.values() if x.node is not worldMap.startNode])
step =0
starttime = time.time()
for obstacle in obstacles :
    step +=1
    newPath = pathBuilder.buildPath([obstacle])
    #print(f"Appending a newPath: {newPath}, looping:{newPath.looping}, outOfBounds:{newPath.outOfBounds}")
    loopingPaths.append((obstacle, newPath)) if newPath.looping else None
    print(f'{step}, {time.time()-starttime:.2f}s') if step%100 == 0 else None
assertExpected(len(loopingPaths), 6)
assertExpected(len(set([x[0] for x in loopingPaths])), 1951)

'''    
data = getInput()
worldMap = WorldMap(data)
path = Path(worldMap.startNode, 'N', worldMap)
path.buildPath()
print(f"Original: {path.startNode}")
assertExpected(len(set([x[0] for x in path.visitedPath])), 41)



#Part 2
begin, timeElapsed = time.time(), 0
stepTime=begin
results = []

for i, p in enumerate(path.visitedPath) :
    #print(f'{i}, {p[0]}, {p[1]}, {path.visitedPath[:i]}')
    if i+1 == len(path.visitedPath) :
        continue
    newObstacle = path.visitedPath[i+1][0] if i+1 < len(path.visitedPath) else None
    newObstacle = newObstacle if newObstacle is not worldMap.startNode else None
    newPath = Path(p[0], p[1], worldMap, visitedPath = path.visitedPath[:i+1], obstacles=[newObstacle] )
    result = newPath.buildPath()
    if result[0] == 'looping' and newObstacle is not None:
        stepTime = time.time()  
        print(f"step:{i}")
        print(f"timeElapsed: {time.time()-stepTime:.2f}s sinceBegin:{stepTime-begin:.2f}") 
        results.append((newObstacle, result))

assertExpected(len(set([x[0] for x in results])), 6, part=2)





class PathBuilder() :
    def __init__(self, startNode, startDirection, worldMap, obstacles=None, visitedPath = None) :
        self.startNode = startNode
        self.startDirection = startDirection
        self.worldMap = worldMap
        obstacles = worldMap.obstacles if obstacles is None else worldMap.obstacles + obstacles
        self.obstacles = set(obstacles)
        self.allNodes = worldMap.allNodes
        self.visitedPath = [] if visitedPath is None else visitedPath
        #self.buildPath()
        
    def getNextNode(self, curNode, direction) :
        nextNode = self.worldMap.getNode(curNode.getNextPosition(direction))
        
        if nextNode in self.obstacles :
            return self.getNextNode(curNode, vector[direction][1])
        
        return nextNode, direction


    def buildPath(self) :
        curNode = self.startNode
        direction = self.startDirection
        
        while curNode :
            self.visitedPath.append((curNode, direction))
            
            curNode, direction = self.getNextNode(curNode, direction)
            if (curNode, direction) in self.visitedPath :
                return "looping", curNode, direction
            if curNode not in self.allNodes :
                return "Out of Bounds", curNode, None
        
        return self

'''
