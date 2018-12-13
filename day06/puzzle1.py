import collections
import colorsys
import itertools
import math  # noqa
import pathlib

from PIL import Image


# Parse the raw input data into tuples of ints
raw = (pathlib.Path(__file__).parent / 'input.txt').open('r').read().strip()
points = [
    tuple(int(n) for n in line.split(', ')) for line in raw.splitlines()
]

# Find the min and max of both dimensions
xMin = min(points, key=lambda c: c[0])[0]
xMax = max(points, key=lambda c: c[0])[0]
xDim = xMax - xMin + 1

yMin = min(points, key=lambda c: c[1])[1]
yMax = max(points, key=lambda c: c[1])[1]
yDim = yMax - yMin + 1

# Adjust the coordinates to start at 0
points = [
    (x - xMin, y - yMin) for x, y in points
]

# Generate unique hues for each point
hues = [
    (137.5077640500378546463487 * i) % 360 for i in range(len(points))
]


# Create an empty grid
# grid = [None for n in range(xDim * yDim)]
grid = [[None for y in range(yDim)] for x in range(xDim)]
infinite = set()

# Compute distances for each point on the grid
for yCoord in range(yDim):
    for xCoord in range(xDim):
        distances = {}
        for i, (xPoint, yPoint) in enumerate(points):
            # Euclidian distance
            # distance = math.sqrt(
            #     (xPoint - xCoord)**2 + (yPoint - yCoord)**2
            # )

            # Manhattan distance
            distance = (
                abs(xPoint - xCoord) + abs(yPoint - yCoord)
            )

            if distance not in distances:
                distances[distance] = []
            distances[distance].append(i)

        shortest = min(distances.keys())
        closest = distances[shortest]

        if len(closest) > 1:
            continue

        closest = closest[0]

        # address = (yCoord * (yDim - 1)) + xCoord
        # print('ADDRESS', address)
        grid[xCoord][yCoord] = closest

        # Identify infinite areas (edges)
        if xCoord in [0, xDim - 1] or yCoord in [0, yDim - 1]:
            infinite.add(closest)

counter = collections.Counter(itertools.chain(*grid))
largest = None
for value, count in counter.most_common():
    if value is None or value in infinite:
        continue
    print(f'The answer is {count}')
    largest = value
    break


canvas = Image.new(
    mode='RGB',
    size=(xDim, yDim),
    color=(255, 255, 255),
)

for yCoord in range(yDim):
    for xCoord in range(xDim):
        # address = (yCoord * (yDim - 1)) + xCoord
        # closest = grid[address]
        closest = grid[xCoord][yCoord]
        if closest is not None:
            lightness = 0.15 if closest in infinite else 0.8
            closest = int(closest)
            if closest == largest:
                canvas.putpixel(
                    xy=(xCoord, yCoord),
                    value=(255, 0, 255),
                )
            else:
                canvas.putpixel(
                    xy=(xCoord, yCoord),
                    value=tuple(
                        int(n * 255) for n in colorsys.hls_to_rgb(
                            hues[closest], lightness, 1.0
                        )
                    ),
                )

for i, point in enumerate(points):
    canvas.putpixel(
        xy=point,
        value=(255, 0, 0),
    )

canvas.show()
