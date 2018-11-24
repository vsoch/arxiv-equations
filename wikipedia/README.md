# Equation Mapping

This is the mapping portion of the project, meaning that we aim to derive vectors (using word2vec)
that describe domains of math and methods, and we will do this based on the equations on the 
page.

## 1. Install Requirements

First, install requirements, including a few libraries I created as a graduate
student, [wordfish](https://vsoch.github.io/2016/2016-wordfish/) and [repofish](https://pypi.org/project/repofish/)
wordfish is a small library that uses gensim to run word2vec, and repofish uses it
to parse various internet resources for words, etc.

```bash
pip install -r requirements.txt
```

## 2 Create List of Math Domains and Methods

We first need to find the "right" wikipedia pages to parse equations from. I'm also interested
in the applications, so I'm parsing methods too. For this step, I used [0.extractEquations.py](0.extractEquations.py).
I save the list of methods to [wikipedia_methods.txt](wikipedia_methods.txt) and equations
to [wikipedia_equations.json](wikipedia_equations.json) along with the similarly named
pickle files (ending in *.pkl). The extraction is fairly easy to do because each equation (an
annotation in the page) has a "fallback" image (with a class with the name including math or tex)
that can be easily extracted! For example:

```python
  {'png': 'https://wikimedia.org/api/rest_v1/media/math/render/svg/b7c3ba47cc5436c389f86a3f617a191d0dbe4877',
   'tex': '2^{n\\mathrm {H} (k/n)}'},
```

This "master" file we can use for one word2vec model, and for a domain specific model (doc2vec)
we can generate a single file under [sentences](sentences) that has the sentences grouped by wikipedia page.

## 3. Extract Equation Tokens

This was very fun to do! I wanted to call a token either a single character, **or** a known
latex string (e.g., `/begin`) and put them together in a sentence for word2vec. I did this using
as the first step in [1.modelEquations.py](1.modelEquations.py).

## 4. Build Word2Vec Equations Models

For the second step (also in [2.modelEquations.py](2.modelEquations.py)) I could 
easily use the functions from [wordfish](https://vsoch.github.io/2016/2016-wordfish/)
to build a word2vec model and extract vectors to describe the tokens. Then, an average
vector could be used to combine a set of features (from a label) to describe the full
equation. I can cluster both the feature (single token) vectors along with the equations,
and see if the method clusters makes sense.

After this step we have:

 - [word2vec models](models) to describe either the entire wikipedia corpus, or subset of domains (pages)
 - [vectors of the embeddings](vectors) that represent the embeddings for the tokens, or individual characters

I actually did the above for all equations (across all wikipedia topics) with word2vec, and for
doc2vec, but I'm going to hold off using doc2vec for anything because I don't totally 
understand what it's doing yet.

## 5. Map Equations to Embedding Space

I have two choices now. I can either take the average of some set of equation vectors that I've derived for
a topic, **or** work in a space with all the vectors (and labels to describe multiple cases of the same topic).
I think I want to try the latter first, because taking some kind of average could dilute the signal.
So as a first sanity check, I'd want to see that equations from the same topic are similar, meaning
that their topics cluster together. So I will do the following:

 - Start with character embeddings that are derived across entire set of equations, across all topics
 - For each topic, for each equation, map it to the space by generating it's vector (an average of it's character embeddings present in the model)
 - Now we have a vector representation (the same length, 300) for every equation!
 - Do clustering of the equation vectors, and (sanity check) the similar labels should cluster together.

I might go back at this point and choose more specific labels for kinds of math, as opposed to the statistics articles list that I chose. When there is a model that seems to be reasonably good, then I can do the same thing, but for equations in archive. For each paper in archive, I can again map the equations it includes to this space, and determine it's
"math topics" signature. These proportions can help us determine the domains of math that are highest priority for
penrose, and it's also just a really cool and interesting question anyway! 
