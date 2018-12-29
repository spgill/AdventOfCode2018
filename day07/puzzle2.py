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

        self.locked = False

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


def valueOf(char):
    return ord(char) - 4


chain = []
edges = []
for node in Step.register.values():
    if len(node.reverse) == 0:
        edges.append(node)


workerCount = 5
workerStacks = [0 for i in range(workerCount)]
workerJobs = [None for i in range(workerCount)]
clock = 0


print(
    f'Time   W1   W2   W3   W4   W5   Done'
)


while len(edges):
    for i in range(workerCount):
        if clock >= workerStacks[i]:
            # Pop off the previous job
            currentJob = workerJobs[i]
            if currentJob is not None:
                workerJobs[i] = None
                chain.append(currentJob)
                edges.remove(currentJob)

                for ancestor in currentJob.forward:
                    if ancestor not in chain and ancestor not in edges:
                        edges.append(ancestor)

            # If there's not any current job
            if workerJobs[i] is None:

                # Sort the edges
                edges.sort(key=lambda n: n.name)

                # Find a new job
                choice = None
                choiceIndex = None
                for edge in edges:
                    if not edge.locked\
                       and all(node in chain for node in edge.reverse):
                        edge.locked = True
                        # workerStacks[i] += valueOf(edge.name)
                        workerStacks[i] = clock + valueOf(edge.name)
                        workerJobs[i] = edge
                        break

    chainText = ''.join([n.name for n in chain])
    workerText = ''
    for i in range(workerCount):
        job = getattr(workerJobs[i], 'name', ' ')
        workerText += f'   {job} '
    print(
        f'{clock: >4}{workerText}   {chainText}'
    )
    # exit()

    clock += 1

workerMax = max(workerStacks)
print(f'The answer is {workerMax}')


