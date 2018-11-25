# Equation Mapping: Math

Here we will derive vectors based on equations from these math topics. While
I ultimately will just want to map these equations to the [statistics](statistics)
space, I will also generate the same character embeddings here to be consistent.

# Step 1. Get equations from Wikipedia

I am using the following list of (domain, topic) from wikipedia:

```bash
# Organized by (AbstractTopic, PageTopic)
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
```

I found these categories and groupings [here](https://en.wikipedia.org/wiki/Areas_of_mathematics#External_links).
The general idea is that the first token is an abstract token (e.g., Linear Algebra and Abstract Algebra are both
kinds of Algreba") and the sceond is the page name to parse. For this parsing I will also try
to minimize dependencies (e.g., removing repofish).

Before starting here you should have already installed the required python
modules in [requirements.txt](../requirements.txt). Since I've already done this for
[statistics](../statistics) articles, I can clean up the code a bit too and make a more succint
pipeline. The entire set of steps will be in [mathDomainAnalysis.py](mathDomainAnalysis.py).

After this step, we have generated [wikipedia_math_articles.json](wikipedia_math_articles.json),
a dictionary with key as method indexing metadata for each page above. 
The biggest difference here between this extraction and the statistics is that I didn't
save any intermediate files.


# Step 2: Extract Equations ####################################################

The above step gave us a list of math articles, and what we want to do now is:
 - retrieve each page as a WikipediaPage
 - parse the html with BeautifulSoup
 - look through the images on the page (some of which are equations) and find them
 - save the list of equations, along with the domain and topic of the page

At the end of this step, we have a dictionary of equations, indexed by method
name, and then content including the tex, png, domain, and topic:

```python
{'domain': 'Geometry',
   'png': 'https://wikimedia.org/api/rest_v1/media/math/render/svg/a1da4e06eb6f25cd7f7fc1a7784a11a82ae53f9f',
   'tex': '\\frac{a-b}{a+b}=\\frac{\\tan\\left[\\tfrac{1}{2}(A-B)\\right]}{\\tan\\left[\\tfrac{1}{2}(A+B)\\right]}',
   'topic': 'Trigonometry'}
```

And we save this dictionary to both [wikipedia_math_equations.json](wikipedia_math_equations.json)
and [wikipedia_math_equations.pkl](wikipedia_math_equations.pkl).


# Step 3: Word2Vec Model #######################################################

At this point, we would actually want to give the equations to the statistics model,
and then generate embeddings for our math equations based on the statistics
character embeddings. I haven't done that yet, but instead I've
created an example showing how to do this for the math equations.
With our equations loaded, we *could* now use the wordfish `TrainEquations` class to
take in the list of equations, and generate a model. That comes down to this:

```python
sentences = TrainEquations(text_list=equations_list,
                           remove_stop_words=False,
                           remove_non_english_chars=False)

model = Word2Vec(sentences, size=300, workers=8, min_count=1)
```

We don't want to mess with removing non english characters or stop words (which
uses nltk to filter, etc.) because we aren't working with a standard English corpus!
At the end of this step, we have a word2vec model, and we can save it under 
[models](models).
