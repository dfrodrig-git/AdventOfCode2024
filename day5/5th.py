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
        

def getInput(test = True, day = 5) :
    if testRun or test :
        f=open(f'inputDay{day}Test.txt')
    else :
        f=open(f'inputDay{day}.txt')
    
    rules = [line.strip().split("|") for line in f if line.find("|") >0]


    if testRun or test :
        f=open(f'inputDay{day}Test.txt')
    else :
        f=open(f'inputDay{day}.txt')

    data = [line.strip().split(",") for line in f if line.find(",")>0]

    return rules, data

class Rule() :
    def __init__(before,after) :
        self.bef = before
        self.aft = after
    def __str__() :
        debug("Rule: {self.bef}|{self.aft}")
    
#Part1
rulesInput, data = getInput()

rules = [Rule(bef,aft) for bef,aft in rulesInput]


#assertExpected(sum([x[2] for x in resultsPart1]), 18)

#Part 2


#assertExpected(sum([x[1] for x in resultsPart2]), 9, part=2)


