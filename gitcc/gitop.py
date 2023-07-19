import subprocess
import datetime
from dateutil import parser
import sys

repo_path = sys.argv[1] 
branch = sys.argv[2]

commits = subprocess.check_output(['git', 'log', '--format=%H %cI', branch], cwd=repo_path)

commits = commits.decode('utf-8').strip().split('\n')

result = []
for commit in commits:
    parts = commit.split(' ')
    # Remove colon from timezone offset
    parts[1] = parts[1].replace('+08:00', '+0800')

    commit_date = datetime.datetime.strptime(parts[1], '%Y-%m-%dT%H:%M:%S%z')
    commit_date = commit_date.strftime("%Y-%m-%d %H:%M:%S")

    commit_hash = parts[0]
    result.append((commit_date, commit_hash))

result.sort(key=lambda x: x[0]) 

print(result)

