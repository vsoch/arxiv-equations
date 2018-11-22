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

```json
  {'png': 'https://wikimedia.org/api/rest_v1/media/math/render/svg/b7c3ba47cc5436c389f86a3f617a191d0dbe4877',
   'tex': '2^{n\\mathrm {H} (k/n)}'},
```

## 3. Build Word2Vec Equations Models

Next, I built a word2vec model for the equations with [2.modelEquations.py](2.modelEquations.py).
