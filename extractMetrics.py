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
import tarfile
from helpers import ( extract_tex, get_metadata, chunks )


# Let's get nltk
import nltk
nltk.download('all')

from nltk import word_tokenize

################################################################################
# Step 1. Test with Input Example
################################################################################

# Example file to work with
input_file = os.path.abspath('0801/0801.4928.tar.gz')

# Extract latex as a long string
tex = extract_tex(input_file)

# Metadata based on uid from filename
uid = os.path.basename(input_file).replace('.tar.gz','')
metadata = get_metadata(uid)

# Extract the equations from the tex
equations = re.findall("\\$.*?(?<!\\\\)\\$", str(tex))

result = {'equations': equations,
          'metadata': metadata,
          'inputFile': input_file,
          'uid': uid}

output_file = input_file.replace('.tar.gz', '.pkl')
pickle.dump(result, open(output_file,'wb'))

# Testing older format

input_file = os.path.abspath('bayes-an/9506/9506003.tar.gz')

# The difference is the identifier for the file
suffix = os.path.basename(input_file).replace('.tar.gz','')
prefix = input_file.split('/')[-3]
uid = '%s/%s' %(suffix, prefix)

# We will write a function to parse uid

################################################################################
# Step 2. Run for Entire Set
################################################################################

input_files = recursive_find('0801', '*tar.gz')

for input_file in input_files:

    print("Parsing %s..." %input_file)

    # Extract latex as a long string
    tex = extract_tex(input_file)

    if tex is not None:

        # Metadata based on uid from filename
        uid = os.path.basename(input_file).replace('.tar.gz','')
        metadata = get_metadata(uid)

        # Extract the equations from the tex
        equations = re.findall("\\$.*?(?<!\\\\)\\$", str(tex))
        metadata['length'] = len(tex)

        result = {'equations': equations,
                  'metadata': metadata,
                  'inputFile': input_file,
                  'latex': tex,
                  'uid': uid}

        output_file = input_file.replace('.tar.gz', '.pkl')
        pickle.dump(result, open(output_file,'wb'))
