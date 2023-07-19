import subprocess
import datetime
from dateutil import parser
import sys

def get_full_commit_list(repo_path, branch):
    try:
        output = subprocess.check_output(['git', 'log', '--date-order','--reverse','--format=%H %cI', branch], cwd=repo_path)
        print(output)
    except subprocess.CalledProcessError as e:
        print(e)
        exit(1)
    except OSError as e:
        print(e)
        exit(1)

    commits = commits.decode('utf-8').strip().split('\n')

    result = []
    for commit in commits:
        parts = commit.split(' ')
        # Remove colon from timezone offset
        parts[1] = parts[1].replace('+08:00', '+0800')

        commit_date = datetime.datetime.strptime(parts[1], '%Y-%m-%dT%H:%M:%S%z')
        commit_date = commit_date.strftime("%Y-%m-%d %H:%M:%S")

        commit_hash = parts[0]
        result.append({'commit_date': commit_date, 'commit_id': commit_hash})
    print(f' Total number of commits: {len(result)}')
    return result

def _take_elements_in_total(lst,steplength):
    if(len(lst)<=steplength):
        return [lst[-1]]
    else:
        result = lst[::steplength]
        # 加入提交时间最近的一个 commit id
        if result[-1]['commit_id'] != lst[-1]['commit_id']:
            result.append(lst[-1])
        return result

def get_commit_list(repo_path, branch,steplength):
    full_list=get_full_commit_list(repo_path, branch)
    ret = _take_elements_in_total(full_list,steplength)
    print(f' Interval of commits : {steplength}')
    print(f' Number of commits picked: {len(ret)}')
    return ret


def checkout_commit(repo_path, commit_id):
    full_commit_id = subprocess.check_output(
        ['git', 'rev-parse', commit_id], cwd=repo_path).decode().strip()
    try:
        output=subprocess.check_output(
        ['git', 'checkout', '-f', full_commit_id], cwd=repo_path)
        print(output)
    except subprocess.CalledProcessError as e:
        print(e)
        exit(1)
    except OSError as e:
        print(e)
        exit(1)

