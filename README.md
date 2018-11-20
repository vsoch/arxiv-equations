# Equation Analysis

This is development of simple analysis to parse a set of papers from [arxiv](https://arxiv.org/help/bulk_data).
Our goals are the following:

 1. to classify equations into groups based on domains of knowledge (math or methods). We will do this by using equations from wikipedia methods pages as a gold standard, and then word2vec (or similar) to represent an equation as a vector.
 2. to classify papers into groups based on the equations, the idea being that a paper mapped to a domain of knowledge can help us to understand:
    - the domains that are assocated with different kinds of math and methods
    - gaps / potential for working on a method for a domain that hasn't been tried yet
    - understanding of what kinds of math are used (and to what degree) across domains, to drive development of Penrose
 3. To develop a visualization (catalog) that can nicely portray how groups of papers map to domains of math / methods, by way of the equations they use (this will be the final result in the [arxiv-catalog](https://www.github.com/vsoch/arxiv-catalog) repository.
 

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
[arxiv catalog](https://vsoch.github.io/arxiv-catalog/). You can see
examples of the metadata extracted by looking at any of the markdown files
in the [posts](https://github.com/vsoch/arxiv-catalog/tree/master/_posts) folder there.
The goal of the "catalog" is to eventually (visually) present summary metrics for
 each category described by archiv (each manuscript has one or more category 
labels like `astro-ph`). I haven't decided how I want to do this yet, but will
develop something after I do a first extraction. My thinking is that we
can hve simple metrics to describe the articles, for example:
 
 - **journal**: The name of the journal
 - **number of authors**: I don't see a logical reason for this to have any association with equations, but you never know.
 - **length of article**: We would need to normalize the number of equations based on the length.

but more interesting would be to do a further analysis to classify the equations
to belong to one or more methods or domains of math. Thus, this is more of a fuzzy clustering. 
This is the first step toward one of the goals outlined above.

### What else are we interested in?
When the above is done, we would be interested in:

 - a total list of categories, and description of metrics by category
 - a breakdown of equations by category
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

### Step 3: Equation Mapping

I realized that in order to map equations to domains of math and methods, we need
some kind of gold standard. Why not use wikipedia? In that wikipedia pages have
clearly defined LaTeX equations (much easier to parse than raw LaTex because they
are in image tags) *and* a clear title for the page, it would be fairly easy
to extract word2vec embeddings for the equations in a page, and then associate
them with the topic. I call this step the "equation mapping" because that is 
exactly what we are doing - mapping topics to equation vectors that will be useful
in the next step of the archive analysis. To help with this, see the 
[wikipedia](wikipedia) folder. 


## Step 4: Topic Extraction

Once we have vector representations of equations for topics, we can use the
word2vec model to derive vectors for each equation represented in the arxiv papers.
The vectors can then be used as features to calculate similarity of each paper
to each wikipedia topic. I hope that we will be able to then say that a particular
paper has some set of methods / domains of math overly represented at a rate
unlikely due to chance. I haven't thought through the details here, but will
do so when I write the code. I can use the following steps on Sherlock to
get an interactive node and load python modules for doing development 
(after cloning the repository into the present working directory).

```bash
# interactive node
srun --time 48:00:00 --mem 32000 --pty bash

# python modules
ml python/3.6.1
ml py-pandas/0.23.0_py36
ml py-ipython/6.1.0_py36
```

I will use ipython to test and run the [extractMetrics.py](extractMetrics.py)
(not written yet).


## Challenges

One challenge I ran into was being able to extract **all** the equations from a 
particular LaTeX document. I was able to derive regular expressions to get most
of them, but never all of them. I was first very discouraged by this. But I realized
that we don't need to perfectly get them all as long as we can get a large sample,
and use the sample to classify the paper.
