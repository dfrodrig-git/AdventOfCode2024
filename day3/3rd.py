import re
from collections import Counter

testExpected1=161
testExpected2=48

def getInput(test = True, day = 3) :
    if test :
        f=open(f'inputDay{day}Test.txt')
    else :
        f=open(f'inputDay{day}.txt')

    p=re.compile(r"mul\((\d+),(\d+)\)")

    

    return p.findall(f.read())

def getInputDont(test = True, day = 3) :
    p=re.compile(r"don\'t\(\)[.*mul\((\d+),(\d+)\)]*do\(\)")

    if test :
        data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
        return p.findall(data)
    else :
        f=open(f'inputDay{day}.txt')
    
    return p.findall(f.read())


#Part 1
result = sum([int(x)*int(y) for x,y in getInput()])

print(f'Result Part1 Test: {result}, while expected is {testExpected1}')

#Part 2
resultDont = sum([int(x)*int(y) for x,y in getInputDont()])

print(f'Result Test: {result-resultDont}, while expected is {testExpected2}')
