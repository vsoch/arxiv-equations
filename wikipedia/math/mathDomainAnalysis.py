#!/usr/bin/env python

from bs4 import BeautifulSoup
from wordfish.utils import ( get_attribute, save_pretty_json )
from wikipedia import WikipediaPage
import pickle
import json
import re
import os

# Now let's derive equations from core mathematics ideas (not statistics articles)
# Organized by (AbstractTopic, PageTopic)

results = dict()

pages = [
 ( "Algrebra", "Linear algebra"),
 ( "Algrebra", "Multilinear_algebra"),
 ( "Algrebra", "Abstract algebra"),
 ( "Algrebra", "Elementary_algebra"),
 ( "Arithmetic", "Number theory"),
 ( "Calculus", "Mathematical analysis"),
 ( "Calculus", "Differential equations"),
 ( "Calculus", "Dynamical systems theory"),
 ( "Calculus", "Numerical analysis"),
 ( "Calculus", "Mathematical optimization"),
 ( "Calculus", "Functional analysis"),
 ( "Geometry", "Discrete geometry"),
 ( "Geometry", "Algebraic geometry"),
 ( "Geometry", "Analytic geometry"),
 ( "Geometry", "Differential geometry"),
 ( "Geometry", "Finite geometry"),
 ( "Geometry", "Topology"), 
 ( "Geometry", "Trigonometry"),
 ( "Foundations of Mathematics", "Philosophy of mathematics"), 
 ( "Foundations of Mathematics", "Mathematical logic"),
 ( "Foundations of Mathematics", "Set theory"),
 ( "Foundations of Mathematics", "Category theory"),
 ( "Applied Mathematics", "Mathematical physics"),
 ( "Applied Mathematics", "Probability theory"),
 ( "Applied Mathematics", "Mathematical statistics"), 
 ( "Applied Mathematics", "Statistics"),
 ( "Applied Mathematics", "Game theory"),
 ( "Applied Mathematics", "Information theory"), 
 ( "Applied Mathematics", "Computer science"),
 ( "Applied Mathematics", "Theory of computation"),
 ( "Applied Mathematics", "Control theory"),
 ( "Others", "Order theory"),
 ( "Others", "Graph theory")]


# Step 1. Get pages (and raw equations) from wikipedia

for pair in pages:
    domain = pair[0]
    method = pair[1]
    if method not in results:

        result = WikipediaPage(method)

        # Show a visual check!
        print("Matching %s to %s" %(method,result.title))
        entry = { 'categories': result.categories,
                  'title': result.title,
                  'method': method,
                  'url': result.url,
                  'summary': result.summary,
                  'images': result.images }

        # We can use links to calculate relatedness
        entry['links'] = get_attribute(result, 'links')
        entry['references'] = get_attribute(result, 'references')

        results[method] = entry


save_pretty_json(results, "wikipedia_math_articles.json")



## STEP 2: EQUATIONS ###########################################################

equations = dict()

for pair in pages:
    domain = pair[0]
    method = pair[1]
    if method not in equations:
        print("Extracting equations from %s" %(method))
        result = WikipediaPage(method)
        html = result.html()
        soup = BeautifulSoup(html, 'lxml')

        equation_list = []

        # Equations are represented as images, they map to annotations
        images = soup.findAll('img')
        for image in images:
            image_class = image.get("class")
            if image_class != None:
                if any(re.search("tex|math",x) for x in image_class):
                    png = image.get("src")
                    tex = image.get("alt")
                    entry = {"png":png,
                             "tex":tex,
                             "domain": domain,  # inefficient to store many times,
                             "topic": method}   # but more conservative
                    equation_list.append(entry)

        if len(equation_list) > 0:
            equations[method] = equation_list


save_pretty_json(equations, "wikipedia_math_equations.json")
pickle.dump(equations, open('wikipedia_math_equations.pkl', 'wb'))


## STEP 3: WORD2VEC MODEL ######################################################

from wordfish.analysis import ( 
    DeepEquationAnalyzer, 
    TrainEquations, 
    Word2Vec, 
    extract_vectors,
    extract_similarity_matrix
)

# Derive a list of all equations
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

sentences = TrainEquations(text_list=equations_list,
                           remove_stop_words=False,
                           remove_non_english_chars=False)

model = Word2Vec(sentences, size=300, workers=8, min_count=1)


# Save things
base_dir = os.getcwd()
output_dir = os.path.join(base_dir, 'models')
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

model.save("%s/wikipedia_math_equations.word2vec" % output_dir)

# Export vectors
vectors_dir = "%s/vectors" % base_dir
if not os.path.exists(vectors_dir):
    os.mkdir(vectors_dir)

vectors = extract_vectors(model)
vectors.to_csv('%s/wikipedia_math_equation_character_vectors.tsv' %vectors_dir, sep='\t')

## STEP 3: Similarity of Characters ############################################

simmat = extract_similarity_matrix(model)
simmat.to_csv('%s/wikipedia_math_equations_character_similarities.tsv' % output_dir, sep='\t')


## STEP 4: EQUATION EMBEDDINGS #################################################

# First let's generate based on specific topic
analyzer = DeepEquationAnalyzer(model)
compiled_embeddings = pandas.DataFrame(columns=range(model.vector_size))

for method, items in equations.items():

    # Create a data frame of embeddings for each
    count = 0
    print("Generating embeddings for method %s" %(method))
    embeddings = pandas.DataFrame(columns=range(model.vector_size))

    for item in items:
        label = "%s|%s|%s" %(item['domain'], method, count)
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
compiled_embeddings.to_csv('%s/compiled_math_embeddings.tsv' % vectors_dir, sep="\t", encoding="utf-8")

# TODO create a mean vector on the level of domains
