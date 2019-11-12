import os

command = 'git checkout aliens'
os.system(command)

command = 'git pull'
os.system(command)

command = 'touch deleteme.txt'
os.system(command)

command = 'git add deleteme.txt'
os.system(command)

command = "git commit -m 'add deletme.txt to test autogit.py'"
os.system(command)

command = 'git push'
