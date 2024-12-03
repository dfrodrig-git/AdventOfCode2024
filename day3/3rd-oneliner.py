import re

p=re.compile(r"mul\((\d+),(\d+)\)")
#part 1
print(f"Result part1: {sum ([int(x)*int(y) for x,y in p.findall(open(f'inputDay3.txt').read())])}")

#part 2
print(sum ([int(x)*int(y) for x,y in p.findall(re.sub("don't\(\).*?do\(\)","",open(f"inputDay3.txt").read(),flags=re.S))])   )

