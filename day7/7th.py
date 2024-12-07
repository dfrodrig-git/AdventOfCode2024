#Advent Of Code 2024 day 7 
#by dfrodrig-git 

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
        

def getInput(test = None, day = 7) :
    if testRun :
        f=open(f'inputDay{day}Test.txt')
    else :
        f=open(f'inputDay{day}.txt')
   
    data = [line.replace(":", " ").strip().split() for line in f] 
        
    return data

equations=getInput()

#making it fun, no string thingys :p
def concatOperation(a,b) :
    return a*(10**(math.floor(math.log(b,10))+1))+b
    
def applyOperation(truthValue, currentValue, remainingNumbers):
    #print(f'applyingOperations to : {truthValue}, {currentValue}, {remainingNumbers} ')
    
    if len(remainingNumbers) == 0 or currentValue > truthValue:
       return truthValue == currentValue    

    #multiply
    #print(f'Apply mult')
    resultMul = applyOperation(truthValue, currentValue*remainingNumbers[0], remainingNumbers[1:])
    #apply sum
    #print(f'Apply Sum {currentValue} + {remainingNumbers[0]}')
    resultSum = applyOperation(truthValue, currentValue+remainingNumbers[0], remainingNumbers[1:])

    resultConcat = applyOperation(truthValue, concatOperation(currentValue, remainingNumbers[0]), remainingNumbers[1:])
    return resultMul + resultSum + resultConcat

result = []
equations = [list(map(int, x)) for x in equations]
step =0
for equation in equations :
    step +=1
    #equation = list(map(, equation))
    print(f'Checking {equation} on step {step}') if step%10 ==0 else None
    result.append((equation[0], applyOperation(equation[0], equation[1], equation[2:])))
    

assertExpected(sum([x[0] for x in result if x[1] >0]), 3749)
assertExpected(sum([x[0] for x in result if x[1] >0]), 11387, part=2)

        
#332 low

