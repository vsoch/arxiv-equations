# Equation Mapping

This is the mapping portion of the project, meaning that we aim to derive vectors (using word2vec)
that describe domains of math and statistical methods, and we will do this based on the equations on the 
page. We will do this for the following topic groups on wikipedia:

 - [statistics](statistics)
 - [mathematics](math)

I think what I eventually want to do is use the larger equation corpus (from statistics) to derive
an embedding vector for each token (a character or latex symbol). Then to get the embeddings that
I'm interested in to compare to equations in Arxiv papers, to map equations in the [math](math)
articles to this space. So - [statistics](statistics) will build the underlying model, and
[math](math) will give it context.

## 1. Install Requirements

For both, you need to first install requirements, including a few libraries I created as a graduate
student, [wordfish](https://vsoch.github.io/2016/2016-wordfish/) and [repofish](https://pypi.org/project/repofish/)
wordfish is a small library that uses gensim to run word2vec, and repofish uses it
to parse various internet resources for words, etc.

```bash
pip install -r requirements.txt
```

Then continue with instructions in the subfolder of choice. The steps are generally the same,
but the second (math) was developed after statistics and is more fitting to the goal (be able
to use the model to predict domains of math based on equations in a text).
