#!/usr/bin/env python

from wordfish.analysis import ( 
    DeepEquationAnalyzer,
    DeepCharacterAnalyzer, 
    extract_vectors,
    Word2Vec
)

import pickle
here = os.path.abspath(os.path.dirname(__file__))

equations = pickle.load(open('../math/wikipedia_math_equations.pkl', 'rb'))
# len(equations)
# 22

# Step 1: Derive a list of all equations. We care about labels this time!
equations_list = []
labels = []
domains = []
for method, eqlist in equations.items():
    for eq in eqlist:
        equations_list.append(eq['tex'])
        domains.append(eq['domain'])
        labels.append(eq['topic'])

# len(labels)
# 889

# Model 1: Latex Expressions and Symbols

# Load model built from statistics equation sentences
model_file = os.path.abspath("%s/../statistics/models/wikipedia_statistics_equations.word2vec" % here)
model = Word2Vec.load(model_file)

# Step 2: Time for equation embeddings!
# We will map the equations from math to character embeddings from statistics.

vectors_dir = "%s/vectors" % here
if not os.path.exists(vectors_dir):
    os.mkdir(vectors_dir)

# First let's generate based on specific topic
analyzer = DeepEquationAnalyzer(model)
compiled_embeddings = pandas.DataFrame(columns=range(model.vector_size))

for method, items in equations.items():

    # Create a data frame of embeddings for each
    count = 0
    print("Generating embeddings for %s" %(method))
    embeddings = pandas.DataFrame(columns=range(model.vector_size))

    for item in items:
        label = "%s.%s.%s" %(item['domain'], method, count)
        tex = item['tex']
        embeddings.loc[label] = analyzer.text2mean_vector(item['tex'])
        count += 1

    method_name = method.replace(' ', '-').replace('/','_')
    file_name = "%s/embeddings_%s.tsv" % ( vectors_dir, method_name )
    embeddings.to_csv(file_name, sep="\t", encoding="utf-8")

    # Save to master data frame
    compiled_embeddings = compiled_embeddings.append(embeddings)

# At the end of this loop, we have a data frame for each set of embeddings
# organized by the math topic. We also have one compiled data frame with all 
# labels.
compiled_embeddings.to_csv('%s/compiled_math_embeddings.tsv' % vectors_dir, sep="\t", encoding="utf-8")


# Model 2: Singule Characters
char_file = os.path.abspath("%s/../statistics/models/wikipedia_statistics_characters.word2vec" % here)
model = Word2Vec.load(char_file)
analyzer = DeepCharacterAnalyzer(model)
all_embeddings = pandas.DataFrame(columns=range(model.vector_size))

for method, items in equations.items():

    # Create a data frame of embeddings for each
    count = 0
    print("Generating embeddings for %s" %(method))
    embeddings = pandas.DataFrame(columns=range(model.vector_size))

    for item in items:
        label = "%s.%s.%s" %(item['domain'], method, count)
        tex = item['tex']
        embeddings.loc[label] = analyzer.text2mean_vector(item['tex'])
        count += 1

    method_name = method.replace(' ', '-').replace('/','_')
    file_name = "%s/character_embeddings_%s.tsv" % ( vectors_dir, method_name )
    embeddings.to_csv(file_name, sep="\t", encoding="utf-8")

    # Save to master data frame
    all_embeddings = all_embeddings.append(embeddings)

# At the end of this loop, we have a data frame for each set of embeddings
# organized by the math topic. We also have one compiled data frame with all 
# labels.
all_embeddings.to_csv('%s/compiled_character_math_embeddings.tsv' % vectors_dir, sep="\t", encoding="utf-8")
