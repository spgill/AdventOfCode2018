import pathlib

cwd = pathlib.Path.cwd()

for i in range(25):
    day = cwd / f'day{i + 1:0>2}'
    day.mkdir(exist_ok=True)

    for j in range(2):
        with (day / f'puzzle{j + 1}.py').open('w') as puzzle:
            puzzle.write("print('I\\'m empty!')")
