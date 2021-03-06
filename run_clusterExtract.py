#!/usr/bin/env python

import os
import pickle
import time
from helpers import ( recursive_find, get_uid )

# git clone https://www.github.com/vsoch/arxiv-equations && cd arxiv-equations
# module load python/3.6.1
# pip install --user -r requirements.txt

base = "/regal/users/vsochat/WORK/arxiv"

# Create directories if they don't exist
os.chdir(base)
output = os.path.join(base, 'analysis')
for dirname in ['.job', '.out', 'analysis', '_posts']:
    if not os.path.exists(dirname):
        os.mkdir(dirname)

database = os.path.abspath('data')

# Step 1. Find all the .tar.gz extracted files
input_files = recursive_find(database, '*.tar.gz')

def count_queue():
    user = os.environ['USER']
    return int(os.popen('squeue -u %s | wc -l' %user).read().strip('\n'))

# Step 2. Generate jobs, add any that don't get to run to list
jobs = []
job_limit = 1000

for input_file in input_files:
    count = count_queue()
    name = get_uid(input_file).replace('/', '-')
    datestr = name.split('.')[0]
    month = datestr[0:2]
    year = datestr[2:]
    output_file = os.path.join(output, month, year, 'extracted_%s.pkl' % name)
    output_dir = os.path.dirname(output_file)
    file_name = ".job/%s.job" %(name)
    if not os.path.exists(output_file):
        if count < job_limit:
            print("Processing %s" % name)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            with open(file_name, "w") as filey:
                filey.writelines("#!/bin/bash\n")
                filey.writelines("#SBATCH --job-name=%s\n" %name)
                filey.writelines("#SBATCH --output=.out/%s.out\n" %name)
                filey.writelines("#SBATCH --error=.out/%s.err\n" %name)
                filey.writelines("#SBATCH --time=60:00\n")
                filey.writelines("#SBATCH --mem=2000\n")
                filey.writelines('module load python/3.6.1\n')
                filey.writelines("python3 clusterExtract.py %s %s\n" % (input_file, output_file))
                filey.writelines("python3 generatePage.py %s\n" % (output_file)) # Output to previous used as input
                filey.writelines("rm %s" % os.path.abspath(file_name))
            os.system("sbatch -p owners .job/%s.job" %name)
        else:
            jobs.append(file_name)
            time.sleep(1)

# Submit remaining

while len(jobs) > 0:
    count = count_queue()
    while count < job_limit:
        job = jobs.pop(0)
        os.system("sbatch -p owners %s" % job)
