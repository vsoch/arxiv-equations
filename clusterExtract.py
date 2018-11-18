#!/usr/bin/env python

import sys
import os
import tarfile

# Read in arguments
from helpers import ( extract_tex, 
                      get_metadata, 
                      find_equations,
                      get_uid )

################################################################################
# Step 1. Test with Input Example
################################################################################

input_file = sys.argv[1]
output_file = sys.argv[2]

# Full path of file to work with
input_file = os.path.abspath(input_file)

# Extract latex as a long string
tex = extract_tex(input_file)

# Metadata based on uid from filename
uid = get_uid(input_file)
metadata = get_metadata(uid)
equations = find_equations(tex)

result = {'equations': equations,
          'metadata': metadata,
          'inputFile': input_file,
          'uid': uid}

pickle.dump(result, open(output_file,'wb'))
