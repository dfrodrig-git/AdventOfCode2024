import re



def checkTestResult( result, expected,part=1):
    print(f'Result {part}: {result}, expected: {expected}')


    
def getInput(test = True, day = 4) :
    if test :
        f=open(f'inputDay{day}Test.txt')
    else :
        f=open(f'inputDay{day}.txt')
    
    data = f.read() 
    data = [line.strip() for line in f]

    #p=re.compile(r"mul\((\d+),(\d+)\)")    
    #data=re.sub(r"don\'t\(\)(?s).*?do\(\)","",data)

    return data



