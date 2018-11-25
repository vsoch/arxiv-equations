#!/usr/bin/env python

from bs4 import BeautifulSoup
from wikipedia import WikipediaPage
from helpers import update_method_name
from wordfish.utils import save_pretty_json, write_file, get_attribute
import pickle
import json
import re
import os

## STEP 1: ARTICLES ############################################################

methods_url = "https://en.wikipedia.org/wiki/List_of_statistics_articles"
topic = "List_of_statistics_articles"
result = WikipediaPage(topic)

# These are actually statistics articles, but lots of equations!
methods = set(result.links)

# These tuples are in the format (<old_name> , <new_name>)

disambiguations = (
    ("A posteriori probability (disambiguation)","posterior probability"),
    ("Correlate summation analysis", "Correlation_sum"),
    ("Data generating process", "data collection"),
    ("Data generating process (disambiguation)", "data collection"),
    ("Deviation analysis", "absolute difference"),
    ("Deviation analysis (disambiguation)", "absolute difference"),
    ("Energy statistics", "E-statistics"),
    ("Energy statistics (disambiguation)", "E-statistics"),
    ("Double exponential distribution", "Laplace distribution"),
    ("Double exponential distribution (disambiguation)", "Laplace distribution"),
    ("Lambda distribution (disambiguation)", "Tukey's lambda distribution"),
    ("Lambda distribution", "Tukey's lambda distribution"),
    ("MANCOVA (disambiguation)", "Multivariate analysis of covariance"),
    ("Mean deviation", "Mean signed deviation"),
    ("Mean deviation (disambiguation)", "Mean signed deviation"),
    ("Safety in numbers (disambiguation)", "Safety in numbers"),
    ("T distribution", "Student's t-distribution"),
    ("T distribution (disambiguation)", "Student's t-distribution"),
    ("Contiguity", "Contiguous distribution"),
    ("Correctness", "Correctness (computer science)"),
    ("Energy statistics","E-statistics"),
    ("Sum of squares", "Sum of squares function"),
    ("Sum of squares (disambiguation)", "Sum of squares function"),
    ('Path space', 'classical Wiener space'),
    ('Path space (disambiguation)', 'classical Wiener space'),
    ('MetaNSUE', 'Meta-analysis')
)

removals = ['The Unscrambler',
            "Player wins",
            "Understanding the patterns in Big Data 'dark matter' with GT data mining"] # missing a url, doesn't parse

# in the list, but wikipedia doesn't have defined
for removal in removals:
    if removal in methods:
        methods.remove(removal)

# This is manual parsing to resolve disambiguation errors, 
# we will have redundancy here but not an issue as results is a dictionary
for pair in disambiguations:
    methods = update_method_name(methods, pair[0], pair[1])

# Save list to file, wikipedia changes!
write_file("wikipedia_statistics_articles.txt", '\n'.join(list(methods)))

## STEP 2: Article Metadata ####################################################

# Now let's generate a data structure with all content, links, etc.
results = dict()

for method in methods:
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
        key = result.url.split('/')[-1]

        results[method] = entry
        

# Save to pickle and json, just for fallback
save_pretty_json(results, "wikipedia_statistics_articles.json")
pickle.dump(results, open('wikipedia_statistics_articles.pkl', 'wb'))
len(results)
# 2807

## Step 3: Equations ###########################################################

equations = dict()

for method in methods:
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
                             "tex":tex}
                    equation_list.append(entry)

        if len(equation_list) > 0:
            equations[method] = equation_list


save_pretty_json(equations, "wikipedia_statistics_equations.json")
pickle.dump(equations, open('wikipedia_statistics_equations.pkl', 'wb'))
# len(equations)
# 1900

## Step 4: Word2Vec Model ######################################################
# Save sentences, still useful to have list of labels too

equation_fh = open("equation_statistics_sentences.txt","w")
labels_fh = open("equation_statistics_labels.txt","w")

for method, equation_list in equations.items():
    for equation in equation_list:
        tex = equation["tex"].replace('\n',' ')
        equation_fh.write("%s\n" % tex)
        labels_fh.write("%s\n" % method)       

equation_fh.close()
labels_fh.close()

# Remove last empty newline
os.system("sed -i '/^$/d' equation_statistics_sentences.txt")
os.system("sed -i '/^$/d' equation_statistics_labels.txt")

# Sanity check - length of files should be equal
os.system('cat equation_statistics_sentences.txt | wc -l')
os.system('cat equation_statistics_labels.txt | wc -l')
# 66436
# 66436

# Now build model - we use all data to train

from wordfish.analysis import ( export_vectors, TrainEquations )

sentences = TrainEquations(text_files=["equation_statistics_sentences.txt"],
                           remove_stop_words=False,
                           remove_non_english_chars=False)
model = Word2Vec(sentences, size=300, workers=8, min_count=1)

# Save model to file
base_dir = os.getcwd()
output_dir = os.path.join(base_dir, 'models')
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

model.save("%s/wikipedia_statistics_equations.word2vec" % output_dir)

# Export vectors
vectors_dir = "%s/vectors" % base_dir
if not os.path.exists(vectors_dir):
    os.mkdir(vectors_dir)

vectors = extract_vectors(model)
# vectors.shape
# (3420, 300)

vectors.to_csv('%s/wikipedia_statistics_equation_character_vectors.tsv' %vectors_dir, sep='\t')

# The next step is to map math equations to this space, see the math subfolder,
# and then the analysis subfolder
