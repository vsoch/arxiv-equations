#!/usr/bin/env python

import os
import pickle

# Here we want to parse the equations to build a word2vec model based on equation symbols
equations = pickle.load(open('wikipedia-equations.pkl', 'rb'))

from wordfish.analysis import ( 
    build_models, 
    save_models, 
    export_models_tsv,
    DeepTextAnalyzer, 
    export_vectors
)

# We want to represent known symbols (starting with //) as words, the rest characters

def extract_tokens(tex):
    '''walk through a LaTeX string, and grab chunks that correspond with known
       identifiers, meaning anything that starts with \ and ends with one or
       more whitespaces, a bracket, a ^ or underscore.
    '''
    regexp = r'\\(.*?)(\w+|\{|\(|\_|\^)'
    tokens = []
    while re.search(regexp, tex) and len(tex) > 0:
        match = re.search(regexp, tex)
        # Only take the chunk if it's starting at 0
        if match.start() == 0:
            tokens.append(tex[match.start():match.end()])
            # And update the string
            tex = tex[match.end():]
        # Otherwise, add the next character to the tokens list
        else:
            tokens.append(tex[0])
            tex = tex[1:]
    return tokens
            

# First save sentences to one massive file
with open("equation_sentences.txt","w") as filey:
    for method, equation_list in equations.items():
        for equation in equation_list:
            tex = equation["tex"].replace('\n',' ')
            tokens = extract_tokens(tex)
            characters = " ".join(tokens)
            filey.writelines("%s\n" % characters)

# Remove empty lines in the file (sort of a hack, yeah :) )
os.system("sed -i '/^$/d' equation_sentences.txt")
