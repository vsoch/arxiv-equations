# Equation Analysis

This is development of simple analysis to parse a set of papers from [arxiv](https://arxiv.org/help/bulk_data).
We will use one *.tar, a collection of papers from a particular month and
year, extracted in the folder [0801](0801) to mean (I think) 2001-08 or January of 2008.
The folder was generated from the tar as follows:

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

## Step 1. Metadata and Text Extraction
To test parsing and extraction of a .tar.gz within, please reference the script
[extractMetrics.py](extractMetrics.py). This first section extracts a single tex file,
meaning equations, tex, and metadata, and the second sections loops over the 
logic to do the remaining. I did the loop extraction for one .tar.gz, and will
use the [clusterExtract.py](clusterExtract.py) and [run_clusterExtract.py](run_clusterExtract.py) 
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
[extractmetrics.py](extractmetrics.py) to generate markdown to populate the 
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

## Metrics of Interest
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

## Step 2: Summary Metrics
When the above is done, we would be interested to derive:

 - a total list of categories, and description of metrics by category
 - a breakdown of equations by category

## Step 3: Analysis

We might want to know:

 - what kind of equations cluster together?
 - what groupings (types) of equations are associated with different topics?
 - how do topics compare with respect to equations used?

## Notes about the data

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

## Step 2. Identify Goals

**Summary Metrics**
I want a table of paper id by features, to be used for different kinds of machine
learning.

**Visualize Papers**

I would want, for any paper (tex file) to be able to quickly "see" the equations.
This should look like a simple Github Pages repository that has urls (based on
the unique id of arxiv) to render (likely with MathJax) the equations from the paper.
