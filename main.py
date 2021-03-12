from datetime import timedelta
from git import Repo
from collections import defaultdict
import matplotlib.pyplot as plt

import os.path
from os import path

if path.exists('./tmp/xxx'):
    repo = Repo("./tmp/xxx")
    # repo = Repo("./tmp/react")
else:
    repo = Repo.clone_from('https://github.com/tiangolo/fastapi.git', './tmp/xxx')
    # repo = Repo.clone_from('https://github.com/facebook/react/', './react')

last_60_days_date = repo.head.commit.committed_datetime.date() - timedelta(31)

commits = []
for commit in repo.iter_commits('master'):
    if str(commit.author) == 'github-actions' or str(commit.author) == 'github-actions[bot]':
        continue
    if commit.committed_datetime.date() <= last_60_days_date:
        break
    commits.append(commit)

################################################################################
dates = []
while last_60_days_date <= repo.head.commit.committed_datetime.date():
    dates.append(last_60_days_date)
    last_60_days_date += timedelta(1)
################################################################################

################################################################################
authors = defaultdict(dict)
for commit in commits:
    author = commit.author
    date = commit.committed_datetime.date()

    if author in authors:
        if date in authors[author]:
            authors[author][date] += 1
        else:
            authors[author][date] = 1
    else:
        authors[author][date] = 1
################################################################################

filtered_authors = defaultdict(dict)
for author, dates_commit_count in authors.items():
    for date in dates:
        if date in dates_commit_count:
            filtered_authors[author][date] = dates_commit_count[date]
        else:
            filtered_authors[author][date] = 0

plot_data = defaultdict(list)
for author, dates_commit_count in filtered_authors.items():
    for _, commit_count in dates_commit_count.items():
        plot_data[author.name].append(commit_count)
################################################################################


###############################################################
plt.style.use('seaborn')

for author, ccounts in plot_data.items():
    plt.plot(dates, ccounts, label=author)

plt.gcf().autofmt_xdate()

plt.legend(ncol=3)
plt.title('Number of commits for the last month')
plt.xlabel("Dates")
plt.ylabel("# of commits")

plt.tight_layout()

plt.show()
