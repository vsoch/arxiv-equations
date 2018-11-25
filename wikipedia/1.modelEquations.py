#!/usr/bin/env python

import os
import pickle
from glob import glob
from helpers import extract_tokens

################################################################################
# Step 1. Extract equation sentences, write to file tokenized (separated by space)

# Here we want to parse the equations to build a word2vec model based on equation symbols
equations = pickle.load(open('wikipedia-equations.pkl', 'rb'))

# Word2vec Input sentences -----------------------------------------------------
# First save sentences to one massive file! This will be for word2vec
# Note - I did a check to ensure no empty token lists were returned
equation_fh = open("equation_sentences.txt","w")
labels_fh = open("equation_sentence_labels.txt","w")

for method, equation_list in equations.items():
    for equation in equation_list:
        tex = equation["tex"].replace('\n',' ')
        tokens = extract_tokens(tex)
        characters = " ".join(tokens)
        equation_fh.write("%s\n" % characters)
        labels_fh.write("%s\n" % method)       

equation_fh.close()
labels_fh.close()

# Remove last empty newline
os.system("sed -i '/^$/d' equation_sentences.txt")
os.system("sed -i '/^$/d' equation_sentence_labels.txt")

# Sanity check - length of files should be equal
os.system('cat equation_sentences.txt | wc -l')
os.system('cat equation_sentence_labels.txt | wc -l')
# 66280
# 66280


# Doc2vec Input sentences -----------------------------------------------------
# Now save sentences with one file per term. This will be for doc2vec

sentence_dir = os.path.join(base_dir, 'sentences')
if not os.path.exists(sentence_dir):
    os.mkdir(sentence_dir)

for method, equation_list in equations.items():
    # NOTE, spaces are replaced with - and forward slash with _
    method_name = method.replace(' ','-').replace('/','_')
    filename = os.path.join(sentence_dir, "sentences_%s.txt" %method_name)
    print('Parsing %s' %method)
    with open(filename, "w") as filey:
        for equation in equation_list:
            tex = equation["tex"].replace('\n',' ')
            # Note - we wouldn't need to do this anymore, I added an EquationTraining
            # class to wordfish.analysis
            tokens = extract_tokens(tex)
            characters = " ".join(tokens)
            filey.write("%s\n" % characters)

################################################################################
# Step 2. Build models (word2vec and doc2vec)
# This first model will use ALL the data to train, and then we will derive
# topic-specific vectors based on averages of the input vectors

from wordfish.analysis import ( 
    train_doc2vec_model,
    train_word2vec_model,
    DeepTextAnalyzer, 
    save_models, 
    export_vectors
)

# We will build lda and word2vec models

base_dir = os.getcwd()
output_dir = os.path.join(base_dir, 'models')
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

models = dict()

# We aren't modeling words, so skip over removal of stop / non-enlish
models['equations_word2vec'] = train_word2vec_model(text_files=['equation_sentences.txt'], 
                                                    remove_stop_words=False,
                                                    remove_non_english_words=False)

# Now train doc2vec - here we want to treat each file of equations as a document
docs = glob('%s/*.txt' %sentence_dir)

# Derive labels
labels = [os.path.basename(x).strip('.txt').strip('sentences_') for x in docs]

# len(docs)
# Out[62]: 1894

models['equations_doc2vec'] = train_doc2vec_model(text_labels=labels,
                                                  text_files=docs,
                                                  remove_non_english_chars=False,
                                                  remove_stop_words=False)

# Save models as vectors
export_models_tsv(models, output_dir)
save_models(models, output_dir)

# Export vectors
vectors_dir = "%s/vectors" % base_dir
if not os.path.exists(vectors_dir):
    os.mkdir(vectors_dir)

export_vectors(models, vectors_dir)

################################################################################
# Step 3. Export similarity matrix (not sure this is useful, but why not)
# It's a similarity matrix between the *characters* so I don't expect it to be

# Save a similarity matrix (this takes some time)
simmat = extract_similarity_matrix(models['equations_word2vec'])
simmat.to_csv('%s/equations_word2vex_similarities.tsv' %output_dir, sep='\t')
