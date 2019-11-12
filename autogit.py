import os

command = 'git checkout aliens'
os.system(command)

command = 'git pull'
os.system(command)

command = 'touch deleteme3.txt'
os.system(command)

command = 'git add deleteme3.txt'
os.system(command)

command = "git commit -m 'add deletme3.txt to test autogit.py'"
os.system(command)

command = 'git push'
os.system(command)
