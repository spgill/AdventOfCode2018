import pathlib


# Parse the raw input data
chain = (pathlib.Path(__file__).parent / 'input.txt').open('r').read().strip()

# Create a list of replacement strings from characters in the alphabet
abet = 'abcdefghijklmnopqrstuvwxyz'
replacements = []
for char in abet:
    replacements.append(char.upper() + char)
    replacements.append(char + char.upper())

attempts = []
for attempt in abet:
    attemptChain = chain
    for repl in [attempt, attempt.upper()]:
        attemptChain = attemptChain.replace(repl, '')

    chainLen = len(attemptChain)
    while True:
        for repl in replacements:
            attemptChain = attemptChain.replace(repl, '')

        if len(attemptChain) == chainLen:
            attempts.append(len(attemptChain))
            break
        chainLen = len(attemptChain)

print(
    f'The answer is {min(attempts)}'
)
