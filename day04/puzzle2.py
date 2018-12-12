import collections
import datetime
import pathlib
import re


# Parse the raw input data
raw = (pathlib.Path(__file__).parent / 'input.txt').open('r').read()
entries = re.findall(r'\[(.+?)\] (?:(?:Guard #(\d+))|(\w+))', raw)

# Convert the entries from tuples to lists
entries = [list(entry) for entry in entries]

# Iterate through entry in the log and convert the timestamp to an object
# Also insert empty entries for each guard ID
guardData = {}
for entry in entries:
    entry[0] = datetime.datetime.strptime(
        entry[0],
        r'%Y-%m-%d %H:%M',
    )
    if entry[1]:
        guardData[entry[1]] = []

# Sort the log entries by timestamp
entries.sort(
    key=lambda e: e[0],
)

# Iterate through the sorted entries and organize the sleep/wake times into
# a list
currentGuard = None
sleepStart = None
for time, guardId, action in entries:
    if guardId:
        currentGuard = guardId
        continue

    if action == 'falls':
        sleepStart = time
        continue

    guardData[currentGuard].append((sleepStart, time))


# Iterate through all the guards, figure out which minutes they slept,
# and whom spent the most of a single minute asleep
guardCounts = {}
for guardId in guardData:
    counter = collections.Counter()
    for start, stop in guardData[guardId]:
        counter.update(range(start.minute, stop.minute))
    highest = counter.most_common(1)
    if highest:
        guardCounts[guardId] = highest[0]

guardMaxId = max(
    guardCounts,
    key=lambda g: guardCounts[g][1],
)

# Print solution information
print(
    f'Guard #{guardMaxId} slept the most on a single minute, by being asleep '
    f'a total of {guardCounts[guardMaxId][1]} times '
    f'on the {guardCounts[guardMaxId][0]} minute mark'
)
print(f'The answer is {int(guardMaxId) * guardCounts[guardMaxId][0]}')
