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
        
def getInput(test = None, day = 8) :
    if testRun :
        f=open(f'inputDay{day}Test.txt')
    else :
        f=open(f'inputDay{day}.txt')
   
    data = [line.replace(":", " ").strip().split() for line in f] 
        
    return data

