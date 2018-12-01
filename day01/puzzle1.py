import pathlib


data = (pathlib.Path(__file__).parent / 'puzzle1-input.txt').open('r').read()

output = sum(
    [int(n) for n in data.splitlines()]
)

print('OUTPUT:', output)
