import pathlib
import re


# Class representing a single step
class Step:
    register = {}

    @classmethod
    def get(self, name):
        if name not in self.register:
            self.register[name] = Step(name)
        return self.register[name]

    def __repr__(self):
        head = '(<- ' if len(self.reverse) else '('
        tail = ' ->)' if len(self.forward) else ')'
        return f'{head}{self.name}{tail}'

    def __init__(self, name):
        self.name = name
        self.reverse = []
        self.forward = []

        self.register[name] = self

    def sort(self):
        self.reverse.sort(key=lambda n: n.name)
        self.forward.sort(key=lambda n: n.name)


# Parse the raw input data
raw = (pathlib.Path(__file__).parent / 'input.txt').open('r').read().strip()
orders = re.findall(r'Step (\w).*?step (\w)', raw)


# Iterate through each order and turn them all into steps
for requirement, name in orders:
    previous = Step.get(requirement)
    current = Step.get(name)

    previous.forward.append(current)
    previous.sort()

    current.reverse.append(previous)
    current.sort()


chain = []
edges = []
for node in Step.register.values():
    if len(node.reverse) == 0:
        edges.append(node)


while len(edges):
    edges.sort(key=lambda n: n.name)

    choice = None
    choiceIndex = None
    for i, edge in enumerate(edges):
        if all(node in chain for node in edge.reverse):
            choice = edge
            choiceIndex = i
            break

    if choice:
        chain.append(choice)
        edges.pop(choiceIndex)

        for ancestor in choice.forward:
            if ancestor not in chain and ancestor not in edges:
                edges.append(ancestor)


answer = ''.join([n.name for n in chain])
print(f'The answer is {answer}')
