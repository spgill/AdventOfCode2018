import itertools
import pathlib


data = (pathlib.Path(__file__).parent / 'puzzle1-input.txt').open('r').read()

numbers = [int(n) for n in data.splitlines()]

frequency = 0
seen = {0}

for num in itertools.cycle(numbers):
    frequency += num

    if frequency in seen:
        print('DUPLICATE FOUND:', frequency)
        break

    seen.add(frequency)
