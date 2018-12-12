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
for entry in entries:
    entry[0] = datetime.datetime.strptime(
        entry[0],
        r'%Y-%m-%d %H:%M',
    )

# Sort the log entries by timestamp
entries.sort(
    key=lambda e: e[0],
)

# Print the header
print(
    'Date   ID    Minute'
)
print(
    '             000000000011111111112222222222333333333344444444445555555555'
)
print(
    '             012345678901234567890123456789012345678901234567890123456789'
)


# Iterate through the sorted entries and organize the sleep/wake times into
# a list
dates = {}
currentGuard = None
sleepStart = None
for time, guardId, action in entries:
    if guardId:
        currentGuard = guardId
        continue

    if action == 'falls':
        sleepStart = time
        continue

    date = sleepStart.date()

    if date not in dates:
        dates[date] = {}

    if currentGuard not in dates[date]:
        dates[date][currentGuard] = []

    dates[date][currentGuard].append((sleepStart, time))

# Iterate through each date and construct the lines to print
for date in sorted(dates.keys()):
    stamp = date.strftime(f'%m-%d')
    for guardId in sorted(dates[date].keys()):
        pips = ['.' for i in range(60)]
        for start, stop in dates[date][guardId]:
            spread = list(range(start.minute, stop.minute))
            for n in spread:
                pips[n] = '#'

        pips = ''.join(pips)
        print(
            f'{stamp}  {guardId:<4}  {pips}'
        )
