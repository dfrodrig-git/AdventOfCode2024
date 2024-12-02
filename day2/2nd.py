import re

def getInput(test = True, day = 2) :
    if test :
        f=open(f'inputDay{day}Test.txt')
    else :
        f=open(f'inputDay{day}.txt')

    data = []
    for line in f :
        data.append(list(map(int, line.split())))
        
    return data


def isSafe(line) :
    print(f"Checking if it is Safe: {line}")
    expectedSize = len(line)-1
    rates = [x-y for (x,y) in zip(line[:-1], line[1:]) if 0 < abs(x-y) < 4]
    #print(f'checking: {rates}')
    if len(rates) < expectedSize :
        return False

    direction = [ x for x in rates if x > 0 ]
    if len(direction) == expectedSize or len(direction) == 0 :
        return True

    return False

def isSafeTolerant(line) :
    #rates = [{level:(x,y, x-y)} for (level,(x,y)) in enumerate(zip(line[:-1], line[1:]))]
    print(f"Checking line: {line}") 
    l=len(line)

    if isSafe(line[1:]) :
        return True
    if isSafe(line[:-1]) :
        return True
    for i in range(l) :
        print(f"Checking if Safe {i}: {line[0:i]+line[i+1:]}")
        if isSafe(line[0:i]+line[i+1:]) :
            return True
    print("Is false!")
    return False


matrix = getInput(False)

safeLines = [x for x in matrix if isSafe(x)]
unsafeLines = [x for x in matrix if x not in safeLines]
tolerantLines = [x for x in unsafeLines if isSafeTolerant(x)]

print(f'Result: {len(safeLines)}')

print(f'Result 2 : {len(safeLines)+len(tolerantLines)}')
