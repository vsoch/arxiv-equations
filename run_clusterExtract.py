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
for dirname in ['.job', '.out', 'analysis']:
    if not os.path.exists(dirname):
        os.mkdir(dirname)

database = os.path.abspath('data')

# Step 1. Generate a lookup table
input_files = recursive_find(database, '*.tar.gz')

# For each container, run a container-diff job
for input_file in input_files:
    name = get_uid(input_file).replace('/', '-')
    output_file = os.path.join(output, 'extracted_%s.pkl' % name)
    if not os.path.exists(output_file):
        print("Processing %s" % name)
        file_name = ".job/%s.job" %(name)
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
            time.sleep(0.1)
            os.system("sbatch -p owners .job/%s.job" %name)
