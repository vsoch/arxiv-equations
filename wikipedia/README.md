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

**in progress**
