import re
p=re.compile(r"mul\((\d+),(\d+)\)")
print(sum ([int(x)*int(y) for x,y in p.findall(re.sub("don't\(\)(?s).*?do\(\)","",open(f"inputDay3.txt").read()))])   )

