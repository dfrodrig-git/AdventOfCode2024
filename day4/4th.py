import re
import logging
import sys
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


testRun = True

def assertExpected( result, expected,part=1):
    logger.info(f'Result part:{part}: {result}, expected: {expected}')
    if result != expected and testRun :
        logger.critical("Unnaceptable!")
        

def getInput(test = True, day = 4) :
    if testRun or test :
        f=open(f'inputDay{day}Test.txt')
    else :
        f=open(f'inputDay{day}.txt')
    
    data = [line.strip() for line in f]
    return data


#==============================================================================
# config
#------------------------------------------------------------------------------
vector= {
    'E' : (0,1),
    'W' : (0,-1),
    'N' : (-1,0),
    'S' : (1,0),
    'SW': (1,-1),
    'SE': (1,1),
    'NW': (-1,-1),
    'NE': (-1,1)
    }

searchWord = "XMAS"

soap = getInput()

MAX_ROWS = len(soap[0])
MAX_COLS = len(soap)
#==============================================================================
        
def walk(x, y, direction, step, word):
    logger.debug(f"Checking {y},{x}, in direction {direction}, step{step}, word:{word} - just compared {word[step]} with {soap[x][y]}")
    x += vector[direction][0]
    y += vector[direction][1]
    step += 1

    if step == len(word) :
        return 1
    if x < 0 or y < 0 or x >= MAX_COLS or y >= MAX_ROWS or step > len(word) :
        return 0
    
    if soap[x][y] == word[step] :
        return walk(x,y,direction,step, word)
   
    return 0
     

def checkCrosses(x,y) :
    if x-1 < 0 or y-1 < 0 or x+1 == MAX_COLS or y+1 == MAX_ROWS :
        return 0

    cross1 = soap[x-1][y-1]+soap[x+1][y+1]
    if cross1 not in ["SM", "MS"] :
        return 0
    
    cross2 = soap[x-1][y+1]+soap[x+1][y-1]
    if cross2 not in ["SM", "MS"]:
        return 0
    
    return 1

#Part1
#get all start indexes
startLocations = []
for y, line in enumerate(soap) :
    [startLocations.append((y,x.start())) for x in re.finditer(searchWord[0], line)]
logger.debug(startLocations)

resultsPart1 =[]
step=0 
for startLocation in startLocations :
    for direction in vector.keys() :
        success=(startLocation, direction, walk(startLocation[0], startLocation[1], direction, 0, searchWord))
        resultsPart1.append(success)

assertExpected(sum([x[2] for x in resultsPart1]), 18)

#Part 2
startLocations = []
for y, line in enumerate(soap) :
    [startLocations.append((y,x.start())) for x in re.finditer("A", line)]
logger.debug(startLocations)

resultsPart2 = []
for startLocation in startLocations :
    success=(startLocation, checkCrosses(startLocation[0], startLocation[1]))
    resultsPart2.append(success)

assertExpected(sum([x[1] for x in resultsPart2]), 9, part=2)


