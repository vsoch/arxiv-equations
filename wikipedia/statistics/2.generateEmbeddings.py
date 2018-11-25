#!/usr/bin/env python

import os
import pickle
from glob import glob
from helpers import extract_tokens
from wordfish.analysis import ( load_model, DeepEquationAnalyzer )

# Question: Are equations from the same topic similar? (they should be)
################################################################################
# Step 1. Map each equation from each topic to the embedding space

# Again start with equations
equations = pickle.load(open('wikipedia-equations.pkl', 'rb'))

# Output Folder for embeddings (should exist from previous script)
vectors_dir = "%s/vectors" % base_dir
model_file = os.path.join('models', 'equations_word2vec.word2vec')

# For each topic, generate the mean vector. We will do this via
# the DeepTextAnalyzer, using the word2vec model derived from all equations
model = load_model(model_file)
analyzer = DeepEquationAnalyzer(model)

compiled_embeddings = pandas.DataFrame(columns=range(model.vector_size))

for method, items in equations.items():

    # Create a data frame of embeddings for each
    count = 0
    print("Generating embeddings for method %s" %(method))
    embeddings = pandas.DataFrame(columns=range(model.vector_size))

    for item in items:
        label = "%s_%s" %(method, count)
        tex = item['tex']
        embeddings.loc[label] = analyzer.text2mean_vector(item['tex'])
        count += 1

    method_name = method.replace(' ', '-').replace('/','_')
    file_name = "%s/embeddings_%s.tsv" % ( vectors_dir, method_name )
    embeddings.to_csv(file_name, sep="\t", encoding="utf-8")

    # This might be a bad idea, we will find out!
    compiled_embeddings = compiled_embeddings.append(embeddings)

# At the end of this loop, we have a data frame for each set of embeddings
# organized by the topic. We also have one compiled data frame with all 
# labels.
compiled_embeddings.to_csv('%s/compiled_embeddings.tsv' %vectors_dir, sep="\t", encoding="utf-8")


