#!/usr/bin/env python
#
# extractMetrics 
# is an example (testing) script to derive a method to extract
# some set of metrics from a compressed arxiv paper. We will choose one of the
# tar.gz provided and extract metrics for it, then loop over all parsers. If the
# set gets too large to be reasonable to work with locally, we can move to a
# cluster.

import json
import os
import pandas
import tarfile
import pickle
from helpers import ( extract_tex, recursive_find, get_equation_counts )

input_files = recursive_find('analysis', '*pkl')

# let's just summarize topics, etc.
topics = pandas.DataFrame()

for input_file in input_files:

    print("Parsing %s..." %input_file)

    result = pickle.load(open(input_file,'rb'))

    #get_equation_counts(result['equations'])

    # First let's just summarize the data
    
