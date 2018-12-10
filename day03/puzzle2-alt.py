import array
import pathlib
import re

from PIL import Image


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

# Find the claim that is whole
multiplier = 255 // max(fabric)
canvas = Image.new(
    size=(dimension, dimension),
    mode='RGB',
    color=(255, 255, 255),
)

for claim in claims:
    posX = int(claim[1])
    posY = int(claim[2])
    sizeX = int(claim[3])
    sizeY = int(claim[4])

    count = 0

    for y in range(sizeY):
        for x in range(sizeX):

            offsetX = posX + x
            offsetY = posY + y

            address = (offsetY * dimension) + offsetX

            value = 255 - (fabric[address] * multiplier)

            color = (value, value, value)

            if claim[0] == '1276':
                color = (255, 0, 0)

            canvas.putpixel(
                xy=(offsetX, offsetY),
                value=color,
            )

canvas.save(pathlib.Path(__file__).parent / 'canvas.png')
