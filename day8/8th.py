#Advent Of Code 2024 day 7 
#by dfrodrig-git 
from itertools import combinations
import logging
import sys
from functools import cmp_to_key
import math
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


testRun = False

def assertExpected( result, expected,part=1):
    logger.info(f'Result part:{part}: {result}, expected: {expected}')
    if result != expected and testRun :
        logger.critical("Unnaceptable!")
        
def getInput(test = None, day = 8) :
    if testRun :
        f=open(f'inputDay{day}Test.txt')
    else :
        f=open(f'inputDay{day}.txt')
   
    data = [line.strip() for line in f] 
        
    return data

class AntiNode() :
    def __init__(self, pos) :
        self.pos = pos 
        
class Antenna() :
    def __init__(self, pos, antennaType) :
        self.type = antennaType
        self.pos = pos
    
    def getVectorTo(self, b) :
        return (b.pos[0]-self.pos[0], b.pos[1]-self.pos[1])
    
    def getAntinodePositions(self, b, checkBoundary = None) :
        vector = self.getVectorTo(b)
        
        positions = []
        for direction, pos in [(-1, self.pos), (+1, b.pos)]:
            while checkBoundary(pos) :
                positions.append(pos)
                pos = (pos[0] + direction*vector[0], pos[1]+direction*vector[1])

        #posAntiNode1 = (self.pos[0] - vector[0], self.pos[1] - vector[1]) 
        #posAntiNode2 = (self.pos[0] + vector[0]*2, self.pos[1] + vector[1]*2)
        
        return positions #[posAntiNode1, posAntiNode2]
    

    def __repr__(self) :
        return f"Antenna {self.type} at {self.pos}"
    
    def __str__(self) :
        return f"Antenna {self.type} at {self.pos}"
    
    
class WorldMap() :
    def __init__(self, data=None) :
        self.nodes = {}
        self.buildMap(data) if data else None

    
    def buildMap(self, dataInput) :
        self.MAX_ROWS = len(dataInput)
        self.MAX_COLS = len(dataInput[0])
        
        for y, line in enumerate(dataInput) :
            yflip = self.MAX_ROWS-y
            for x, value in enumerate(line) :
                self.nodes[(x,yflip)] = Antenna((x,yflip), value) if value != "." else None
    
    def getNode(self, pos) :
        return self.nodes.get(pos, None)
    
    def positionInBounds(self, pos) :
        return pos in self.nodes 
        

result = 0
data = getInput()

worldMap = WorldMap(data)

antinodes = [] #type, antinodes
antennas = [x for x in worldMap.nodes.values() if x]

antennaTypeDict = {}
[antennaTypeDict.setdefault(a.type, []).append(a) for a in antennas]
    
for k, v in antennaTypeDict.items() :
    antennaPairs = list(combinations(v,2))
    for a, b in antennaPairs :
        antinodes += [(x, a.type) for x in a.getAntinodePositions(b, worldMap.positionInBounds)]
        
results = set([x for x,y in antinodes if x in worldMap.nodes])

assertExpected(len(results), 14, part=1)

assertExpected(len(results), 34, part=2)

