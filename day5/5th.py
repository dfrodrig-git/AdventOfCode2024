import re
import logging
import sys
from functools import cmp_to_key
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


testRun = False

def assertExpected( result, expected,part=1):
    logger.info(f'Result part:{part}: {result}, expected: {expected}')
    if result != expected and testRun :
        logger.critical("Unnaceptable!")
        

def getInput(test = None, day = 5) :
    if testRun :
        f=open(f'inputDay{day}Test.txt')
    else :
        f=open(f'inputDay{day}.txt')
    
    rules = [list(map(int, line.strip().split("|"))) for line in f if line.find("|") >0]

    if testRun or test :
        f=open(f'inputDay{day}Test.txt')
    else :
        f=open(f'inputDay{day}.txt')

    data = [list(map(int, line.strip().split(","))) for line in f if line.find(",")>0]
    
    return rules, data


class ConstraintMap() :
    def __init__(self, rules) :
        self.buildMap(rules)

    def buildMap(self, rules):
        self.before={}
        self.after={}
        for bef,aft in rules :
            self.before.setdefault(aft, []).append(bef)
            self.after.setdefault(bef, []).append(aft)
        #logger.debug(f"Maps have been built: \nbefore:{self.before}, \nafter:{self.after}")
    
    def compare(self, x,y):
        #print(f'comparign {x}, {y}')
        if y in self.after.get(x, []) :
            return 1
        if y in self.before.get(x, []) :
            return -1
        
        return 0
        
def checkConstraints(value, setBef, setAft, cmap ) :
    #logger.debug(f"Checking value:{value}, setBef:{setBef}, setAft:{setAft}")
    if len (set(cmap.after.get(value, [])) & setBef ) > 0:
        return False
    if len(set(cmap.before.get(value,[])) & setAft ) > 0:
        return False
    return True

def validateUpdate(updateList, constraintsMap) :
    #logger.info(f"Validating {updateList}")
    for i, v in enumerate(updateList) :
        if checkConstraints(v, set(updateList[:i]), set(updateList[i+1:]), constraintsMap) == False:
            return False
    return updateList   

def computeResult(validatedList) :
    #logger.debug(f"validatedList: {validatedList}")
    return sum([x[int(len(x)/2)] for x in validatedList if x is not False])


rules, data = getInput(False)
cmap = ConstraintMap(rules)

#Part1
validatedLists = [validateUpdate(x, cmap) for x in data if x is not False]
assertExpected(computeResult(validatedLists),143) 

#Part 2
unordered = [x for x in data if x not in validatedLists]
#logger.debug(f"Unordered: {unordered} ")
for x in unordered :
    x.sort(key=cmp_to_key(cmap.compare))
    #logger.debug(f'reordered:{x}')
    
assertExpected(computeResult(unordered),123, part=2) 


