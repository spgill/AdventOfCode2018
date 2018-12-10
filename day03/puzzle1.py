import array
import pathlib
import re


data = (pathlib.Path(__file__).parent / 'input.txt').open('r').read()
claims = re.findall(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', data)

# First, we need to construct an array
dimension = 1000
fabric = array.array('B', [0 for n in range(dimension ** 2)])

# Log each claim in the fabric
for claim in claims:
    posX = int(claim[1])
    posY = int(claim[2])
    sizeX = int(claim[3])
    sizeY = int(claim[4])

    for y in range(sizeY):
        for x in range(sizeX):

            offsetX = posX + x
            offsetY = posY + y

            address = (offsetY * dimension) + offsetX

            fabric[address] += 1

# Count the totals
count = 0
for inch in fabric:
    if inch >= 2:
        count += 1

print('RESULT:', count)
