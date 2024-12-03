import re
from collections import Counter

testExpected1=161
testExpected2=48

def getInput(test = True, day = 3, filterDo=True) :
    if test :
        f=open(f'inputDay{day}Test.txt')
    else :
        f=open(f'inputDay{day}.txt')
    
    data = f.read()

    p=re.compile(r"mul\((\d+),(\d+)\)")
    if filterDo :
        data=re.sub(r"don\'t\(\)(?s).*?do\(\)","",data)

    return p.findall(data)


#Part 1
result = sum([int(x)*int(y) for x,y in getInput()])

print(f'Result Part1 Test: {result}, while expected is {testExpected1}')

#Part 2
resultTest= sum([int(x)*int(y) for x,y in getInput(test=True, filterDo=True)])
print(f'Result Part2 Test: {resultTest}, while expected is {testExpected2}')

result= sum([int(x)*int(y) for x,y in getInput(test=False, filterDo=True)])
print(f'Result: {result}')
