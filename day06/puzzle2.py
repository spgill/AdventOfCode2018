import collections
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

# Create an empty grid
grid = [[False for y in range(yDim)] for x in range(xDim)]
infinite = set()

# Compute distances for each point on the grid
for yCoord in range(yDim):
    for xCoord in range(xDim):
        distances = []
        for i, (xPoint, yPoint) in enumerate(points):
            # Euclidian distance
            # distances.append(math.sqrt(
            #     (xPoint - xCoord)**2 + (yPoint - yCoord)**2
            # ))

            # Manhattan distance
            distances.append(
                abs(xPoint - xCoord) + abs(yPoint - yCoord)
            )

        if sum(distances) < 10000:
            grid[xCoord][yCoord] = True

counter = collections.Counter(itertools.chain(*grid))
print(f'The answer is {counter[True]}')


canvas = Image.new(
    mode='RGB',
    size=(xDim, yDim),
    color=(255, 255, 255),
)

for yCoord in range(yDim):
    for xCoord in range(xDim):
        if grid[xCoord][yCoord]:
            canvas.putpixel(
                xy=(xCoord, yCoord),
                value=(0, 0, 0)
            )

for i, point in enumerate(points):
    canvas.putpixel(
        xy=point,
        value=(255, 0, 0),
    )

canvas.show()
