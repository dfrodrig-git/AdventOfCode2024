import re

def checkTestResult( result, expected,part=1):
    print(f'Result part:{part}: {result}, expected: {expected}')

    
def getInput(test = True, day = 4) :
    if test :
        f=open(f'inputDay{day}Test.txt')
    else :
        f=open(f'inputDay{day}.txt')
    
    data = [line.strip() for line in f]
    return data

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

soap = getInput(test=False)

MAX_ROWS = len(soap[0])
MAX_COLS = len(soap)

def walk(x, y, direction, step, word):
    #print(f"Checking {y},{x}, in direction {direction}, step{step}, word:{word} - just compared {word[step]} with {soap[x][y]}")
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
       
#get all start indexes
startLocations = []
for y, line in enumerate(soap) :
    [startLocations.append((y,x.start())) for x in re.finditer(searchWord[0], line)]
#print(startLocations)

results =[]
step=0 
for startLocation in startLocations :
    for direction in vector.keys() :
        success=(startLocation, direction, walk(startLocation[0], startLocation[1], direction, 0, searchWord))
        results.append(success)
#print(results)
checkTestResult(sum([x[2] for x in results]), 18)


#Part 2

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
    
startLocations = []
for y, line in enumerate(soap) :
    [startLocations.append((y,x.start())) for x in re.finditer("A", line)]
#print(startLocations)

results = []
for startLocation in startLocations :
    success=(startLocation, checkCrosses(startLocation[0], startLocation[1]))
    results.append(success)
#print(results)

checkTestResult(sum([x[1] for x in results]), 9, part=2)


