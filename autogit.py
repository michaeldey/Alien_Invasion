import os

commands = []
commands.append('git checkout aliens')
commands.append('git pull')
commands.append('touch deleteme3.txt')
commands.append('git add deleteme3.txt')
commands.append("git commit -m 'add deletme3.txt to test autogit.py'")
commands.append('git push')

for command in commands:
    print(command)
    os.system(command)
