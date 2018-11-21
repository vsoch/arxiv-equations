from repofish.utils import ( save_json, save_txt, convert_unicode )
from repofish.wikipedia import get_page
from exceptions import KeyError
import pandas
import numpy
import time

## STEP 1: PARSE METHOD TEXT ###################################################

methods_url = "https://en.wikipedia.org/wiki/List_of_statistics_articles"
topic = "List_of_statistics_articles"
result = get_page(topic)

# Save list of methods in case it changes
methods = pandas.DataFrame()
methods["methods"] = result.links

# This is manual parsing to resolve disambiguation errors - we will have redundancy here, 
# but not an issue as results object is a dictionary
methods[methods.methods=="A posteriori probability (disambiguation)"] = "posterior probability"
methods[methods.methods=="ANCOVA"] = "Analysis of covariance" # ANCOVA would return "Angola"
methods[methods.methods=="Data generating process"] = "data collection"
methods[methods.methods=="Data generating process (disambiguation)"] = "data collection"
methods[methods.methods=="Deviation analysis"] = "absolute difference"
methods[methods.methods=="Deviation analysis (disambiguation)"] = "absolute difference"
methods[methods.methods=="Double exponential distribution"] = "Laplace distribution"
methods[methods.methods=="Double exponential distribution (disambiguation)"] = "Laplace distribution"
methods[methods.methods=="Lambda distribution (disambiguation)"] = "Tukey's lambda distribution"
methods[methods.methods=="Lambda distribution"] = "Tukey's lambda distribution"
methods[methods.methods=="Linear least squares"] = "Linear least squares (mathematics)"
methods[methods.methods=="Linear least squares (disambiguation)"] = "Linear least squares (mathematics)"
methods[methods.methods=="MANCOVA"] = "Multivariate analysis of covariance"
methods[methods.methods=="MANCOVA (disambiguation)"] = "Multivariate analysis of covariance"
methods[methods.methods=="Mean deviation"] = "Mean signed deviation"
methods[methods.methods=="Mean deviation (disambiguation)"] = "Mean signed deviation"
methods[methods.methods=="Safety in numbers (disambiguation)"] = "Safety in numbers"
methods[methods.methods=="Safety in numbers"] = "Safety in numbers"
methods[methods.methods=="T distribution"] = "Student's t-distribution"
methods[methods.methods=="T distribution (disambiguation)"] = "Student's t-distribution"
methods[methods.methods=="Analyse-it"] = 'Analyze (imaging software)'

methods.to_csv("wikipedia_methods.tsv",sep="\t",encoding="utf-8")

# Now let's generate a data structure with all content, links, etc.
results = dict()

def get_attribute(entry, name):
    try:
        if hasattr(result, name):
            return getattr(result, name)

    # no links :)
    except KeyError:
        pass
    return []

for method in methods["methods"]:
    if method not in results:
        result = get_page(method)

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

# Not sure why this is under statistics
del results["Safety in numbers"]
save_json(results, "wikipedia_methods.json")
len(results)
#2786


## STEP 2: BUILD MODELS ########################################################

print('Vanessasaur, write me!')
