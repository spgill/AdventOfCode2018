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

# Calculate total sleep time for each guard, and then find the highest
guardTotals = {}
for guardId in guardData:
    guardTotals[guardId] = sum(
        (stop - start).seconds / 60 for start, stop in guardData[guardId]
    )
guardMaxId = max(guardTotals, key=lambda g: guardTotals[g])
print(
    f'Guard #{guardMaxId} slept the most, totalling '
    f'{guardTotals[guardMaxId]} minutes'
)

# Iterate through the sleepiest guard's times to find the most likely
# minutes they will be asleep
counter = collections.Counter()
for start, stop in guardData[guardMaxId]:
    counter.update(range(start.minute, stop.minute))
common = counter.most_common(1)[0][0]
print(
    f'Guard #{guardMaxId} slept the most during minute {common}'
)

# The solution is now evident
print(f'The answer is {int(guardMaxId) * common}')
