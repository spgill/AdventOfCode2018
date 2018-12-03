import itertools
import pathlib

dataPath = pathlib.Path(__file__).parent / 'input.txt'
data = dataPath.open('r').read()


def difference(lineA, lineB):
    diff = []
    for i in range(len(lineA)):
        if lineA[i] != lineB[i]:
            diff.append(i)
    return diff


for lineA, lineB in itertools.combinations(data.splitlines(), 2):
    diff = difference(lineA, lineB)
    if len(diff) == 1:
        diff = diff[0]
        common = lineA[:diff] + lineA[diff + 1:]
        print('COMMON CHARACTERS:', common)
        break
