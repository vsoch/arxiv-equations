#!/usr/bin/env python

import os
import pickle


################################################################################
# Step 1. Extract equation sentences, write to file tokenized (separated by space)

# Here we want to parse the equations to build a word2vec model based on equation symbols
equations = pickle.load(open('wikipedia-equations.pkl', 'rb'))

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

    # When we get down here, the regexp doesn't match anymore! Add remaining
    if len(tex) > 0:
        tokens = tokens + [t for t in tex]
    return tokens
            
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
            tokens = extract_tokens(tex)
            characters = " ".join(tokens)
            filey.write("%s\n" % characters)


################################################################################
# Step 2. Build models (word2vec and doc2vec)
# This first model will use ALL the data to train, and then we will derive
# topic-specific vectors based on averages of the input vectors

from wordfish.analysis import ( 
    build_models, 
    save_models, 
    export_models_tsv,
    DeepTextAnalyzer, 
    export_vectors
)

# We will build lda and word2vec models

base_dir = os.getcwd()
output_dir = os.path.join(base_dir, 'models')
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

models = dict()

corpus = {"methods_word2vec" % method_name:["equation_sentences.txt"]}

# We aren't modeling words, so skip over removal of stop / non-enlish
model = build_models(corpus, 
                     model_type="equations_word2vec",
                     remove_stop_words=False,
                     remove_non_english_words=False)

models.update(model)

# Now train doc2vec - here we want to generate one

# Save models as vectors
export_models_tsv(models, output_dir)
save_models(models, output_dir)

#vectors_dir = "%s/analysis/models/vectors" %base_dir
#os.mkdir(vectors_dir)
#export_vectors(models,output_dir=vectors_dir)

## Now for each method, save a vector representation
vectors = pandas.DataFrame(columns=range(300))
model = models["methods_word2vec"]
tempfile = "/tmp/repofish.txt"
analyzer = DeepTextAnalyzer(model)

for method,result in results.iteritems():
    print "Generating model for method %s" %(method)
    summary = convert_unicode(result["summary"]).replace("\n"," ")
    save_txt(summary,tempfile)
    vectors.loc[method] = analyzer.text2mean_vector(tempfile)


vectors.to_csv("%s/method_vectors.tsv" %model_dir,sep="\t",encoding="utf-8")

# Compare similarity, for kicks and giggles
sim = vectors.T.corr()
sim.to_csv("%s/method_vectors_similarity.tsv" %model_dir,sep="\t",encoding="utf-8")


# STOPPED HERE - wordfish needs to be updated for python :3)
