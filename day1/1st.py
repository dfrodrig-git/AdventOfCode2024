import re
from collections import Counter

def getInput(test = True, day = 0) :
    if test :
        f=open(f'inputDay{day}Test.txt')
    else :
        f=open(f'inputDay{day}.txt')

    p=re.compile('(\d+)\s*(\d+)')
    a = []
    b = []
    for line in f :
        #print(f'{p.findall(line)}')
        x, y = map(int,p.findall(line)[0])
        a.append(x)
        b.append(y)

    return a,b


a, b = getInput(test=False, day=1)

#Part 1
a.sort()
b.sort()
result = sum([abs(x-y) for (x,y) in zip(a,b)])

print(f'Result: {result}')

#Part 2
similarity = Counter(b)
result = sum([x*similarity[x] for (x,y) in zip(a,b)])

print(f'Result part 2 : {result}')
