import pathlib


# Parse the raw input data
chain = (pathlib.Path(__file__).parent / 'input.txt').open('r').read().strip()

# Create a list of replacement strings from characters in the alphabet
abet = 'abcdefghijklmnopqrstuvwxyz'
replacements = []
for char in abet:
    replacements.append(char.upper() + char)
    replacements.append(char + char.upper())

chainLen = len(chain)
while True:
    for repl in replacements:
        chain = chain.replace(repl, '')

    if len(chain) == chainLen:
        print(f'The answer is {len(chain)}')
        break
    chainLen = len(chain)
