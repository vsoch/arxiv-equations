from repofish.utils import ( save_json, save_txt, convert_unicode )
from repofish.wikipedia import get_page
from wikipedia import WikipediaPage
from exceptions import KeyError

## STEP 1: METHODS #############################################################
#  Get a list of (disambiguated) methods from Wikipedia

methods_url = "https://en.wikipedia.org/wiki/List_of_statistics_articles"
topic = "List_of_statistics_articles"
result = WikipediaPage(topic)

# Save list of methods in case it changes
methods = set(result.links)


def update_method_name(methods, old_name, new_name):
    '''update the set by removing an old name (usually a disambuguation error)
       with a new name

       Parameters
       ==========
       methods: the set of methods
       oldName: the name to remove
       newName: the name to add
    '''
    if old_name in methods:
        methods.remove(old_name)
    methods.add(new_name)
    return methods

# These tuples are in the format (<old_name> , <new_name>)

disambiguations = (
    ("A posteriori probability (disambiguation)","posterior probability"),
    ("Data generating process", "data collection"),
    ("Data generating process (disambiguation)", "data collection"),
    ("Deviation analysis", "absolute difference"),
    ("Deviation analysis (disambiguation)", "absolute difference"),
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
    ("Sum of squares (disambiguation)", "Sum of squares function")
)


# This is manual parsing to resolve disambiguation errors, 
# we will have redundancy here but not an issue as results is a dictionary
for pair in disambiguations:
    methods = update_method_name(methods, pair[0], pair[1])

removals = ['MetaNSUE', 'Player wins']

# in the list, but wikipedia doesn't have defined
for removal in removals:
    methods.remove(remove)

# Save list to file, wikipedia changes!
save_txt('\n'.join(list(methods)), "wikipedia_methods.txt")

# Now let's generate a data structure with all content, links, etc.
results = dict()

def get_attribute(entry, name):
    '''in the case that a result object doesn't links or references, it would
       throw an error. So check first.'''
    try:
        if hasattr(result, name):
            return getattr(result, name)    
    except KeyError:
        pass
    return []

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

        results[method] = entry

# Not sure why this is under statistics
del results["Safety in numbers"]
save_json(results, "wikipedia_methods.json")
len(results)
#2786


## STEP 2: BUILD MODELS ########################################################

print('Vanessasaur, write me!')
