import collections
import colorsys
import math
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
grid = [None for n in range(xDim * yDim)]
canvas = Image.new(
    mode='RGB',
    size=(xDim, yDim),
    color=(255, 255, 255),
)

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

        address = (yCoord * yDim) + xCoord
        grid[address] = closest

        canvas.putpixel(
            xy=(xCoord, yCoord),
            value=tuple(
                int(n * 255) for n in colorsys.hls_to_rgb(
                    hues[closest], 0.9, 1.0
                )
            ),
        )

for i, point in enumerate(points):
    canvas.putpixel(
        xy=point,
        value=(255, 0, 0),
    )

counter = collections.Counter(grid)
largest = counter.most_common(1)[0][1]
print(f'The answer is {largest}')

# for y in range(64):
#     pips = []
#     for x in range(64):
#         address = (y * yDim) + x
#         value = grid[address]
#         if value is None:
#             pips.append('XX')
#         else:
#             pips.append(f'{value:02X}')
#     print(' '.join(pips))

canvas.show()
