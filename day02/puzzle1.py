import pathlib
import re

dataPath = pathlib.Path(__file__).parent / 'input.txt'
data = dataPath.open('r').read()

abet = 'abcdefghijklmnopqrstuvwxyz'

doubleCount = 0
for line in data.splitlines():
    for char in abet:
        found = re.findall(char, line)
        count = len(found)

        if count == 2:
            doubleCount += 1
            break

tripleCount = 0
for line in data.splitlines():
    for char in abet:
        found = re.findall(char, line)
        count = len(found)

        if count == 3:
            tripleCount += 1
            break

print('CHECKSUM', doubleCount * tripleCount)
