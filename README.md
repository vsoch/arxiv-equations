# Equation Analysis

This is development of simple analysis to parse a set of papers from [arxiv](https://arxiv.org/help/bulk_data).
Our goals are the following:

 - to classify equations into groups based on domains of knowledge (math or methods). We will do this by using equations from wikipedia methods pages as a gold standard, and then word2vec (or similar) to represent an equation as a vector.
 - to classify papers into groups based on the equations, the idea being that a paper mapped to a domain of knowledge can help us to understand:
    - the domains that are assocated with different kinds of math and methods
    - gaps / potential for working on a method for a domain that hasn't been tried yet
    - understanding of what kinds of math are used (and to what degree) across domains, to drive development of Penrose
 

## Step 1. Testing Extraction
We will use one *.tar, a collection of papers from a particular month and
year, extracted to a local folder `0801` (not included in the repository) to mean 
January of 2008. The arxiv files were obtained in bulk and procesed both locally 
and on the Sherlock cluster. The folder was generated from the tar as follows:

```bash
tar -xvf 0801.tar
```

More information about naming is [here](https://arxiv.org/help/bulk_data_s3). 
For example, the description of the folder name:

```bash
Two digit year and month of items in the tar package. Starts with 9108 for 1991-08, rolls past y2k to 0001 for 2000-01, 1008 for 2010-08 etc.
```

Within the single folder, we have over 4000 files!

```bash
$ ls 0801 | wc -l
4516
```

To test parsing and extraction of a .tar.gz within, please reference the script
[testExtract.py](testExtract.py). This first section extracts a single tex file,
meaning equations, tex, and metadata, and the second sections loops over the 
logic to do the remaining. I did the loop extraction for one .tar.gz and it produced
9009 .tar.gz within, meaning 9009 papers (each with a LaTeX file.

## Step 2. Metadata and Text Extraction
Once the extraction method was reasonable (meaning that while I didn't get all
equations with a regular expression, I did get most equations), I wanted to
run the analysis on the [Sherlock cluster](https://www.sherlock.stanford.edu/) at Stanford, and I used the scripts
[clusterExtract.py](clusterExtract.py) and [run_clusterExtract.py](run_clusterExtract.py) 
to do this in parallel for all the .tar.gz. The files were uploaded to the cluster
with scp, and then extracted as follows:

```bash
for tarfile in $(ls *.tar)
    do
       if [ ! -d "${tarfile%.tar}" ]; then
           tar -xf $tarfile
           echo "Extracting $tarfile"
       fi
done
```

The run script also runs 
[generatePage.py](generatePage.py) to generate markdown to populate the 
[arxiv catalog](https://vsoch.github.io/arxiv-catalog/).

The metadata from arxiv includes:
  - id 
  - guidislink
  - updated
  - updated_parsed
  - published
  - published_parsed
  - title
  - title_detail
  - summary
  - summary_detail
  - authors
  - author_detail
  - author
  - arxiv_comment
  - links
  - arxiv_primary_category
  - tags
  - pdf_url
  - affiliation
  - arxiv_url
  - journal_reference
  - doi

### Metrics of Interest

The extraction above, along with the metadata list shown above, also extracts the tex as a 
string, the length, and a list of equation strings.  This isn't a comprehensive list, 
but I'll make some notes about metrics that are important.

 - **topics or domain of the publication**: this could be determined from the metadata, or by parsing the text itself and doing some kind of tokenization.
 - **journal**: The name of the journal
 - **number of authors**: I don't see a logical reason for this to have any association with equations, but you never know.
 - **length of article**: We would need to normalize the number of equations based on the length.

To start (and visualize what we have) it would be useful to generate an index of equations by article.
It would also be fun to see if we can group articles based on equations, and go further to classify equations and
then identify which domains use which kinds of equations.

### What are we interested in?
When the above is done, we would be interested to derive:

 - a total list of categories, and description of metrics by category
 - a breakdown of equations by category

We might want to know:

 - what kind of equations cluster together?
 - what groupings (types) of equations are associated with different topics?
 - how do topics compare with respect to equations used?

### Notes about the data

**Some entries are withdrawals**

And this corresponds to no latex. For example,

```
<TarInfo '0801.0528/p-withdraw' at 0x7f4ada4d8cc8>
```
would return `None`, and should thus be skipped. Another common pattern 
was to find a txt file with a note about the paper being withdrawn:

```
'%auto-ignore\r\nThis paper has been withdrawn by the author,\r\ndue a publication.'
```

**Some LaTex files end in TEX**

And so the function should convert to lowercase before any string checking.

### What are some potential goals?

**Summary Metrics**

I want a table of paper id by features, to be used for different kinds of machine
learning.

**Visualize Papers**

I would want, for any paper (tex file) to be able to quickly "see" the equations.
This should look like a simple Github Pages repository that has urls (based on
the unique id of arxiv) to render (likely with MathJax) the equations from the paper.

## Step 3: Extraction

One challenge I ran into was being able to extract **all** the equations from a 
particular LaTeX document. I was able to derive regular expressions to get most
of them, but for particular papers missed what seems like a substantial subset.
For this reason, I stopped parsing at about 50K papers, mainly to do a first
dummy extraction of the sample. This sample will likely be biased to the .tar.gz
that I did extract, which are organized by date.

This is how I asked for an interactive node:

```bash
srun --time 48:00:00 --mem 32000 --pty bash

ml python/3.6.1
ml py-pandas/0.23.0_py36
ml py-ipython/6.1.0_py36
```
And then I used ipython to test and run the [extractMetrics.py](extractMetrics.py)

## Challenges

We want to identify arxiv domains that are associated with kinds of equations so
that we can programmatically identify which are important. (and write styles for
penrose). The problem we run into is finding the equations in a paper - we don't
have a gold standard set to train on, and regular expressions don't capture them 
all. We can either choose to work with a biased subset (via regular expressions)
or derive a model that is able to find the equations in latex. Possibly an avenue
to do this would be using equations in wikipedia, which are clearly labeled in 
the text. Wikipedia would also give us equations associated with kinds of methods
or math, so we could build some kind of character-based embedding to classify
new equations.

### Step 4: Equation Mapping

We would want to be able to classify the equations in a paper to one or more
domains. to help with this, see the [wikipedia](wikipedia) folder. For this
sub-analysis, we will build a word2vec model that represents equations (in LaTeX)
as vectors, and do this for the equations defined for each wikipedia topic. 
We will then, for each paper equation, use our word2vec model to generate
an equivalent vector for the equation in question, and calculate similarity of 
the vector to the various methods / domains to classify it. I would want to be
able to give an equation to the model and then based on the vector comparison
know the domains it is most similar to.
