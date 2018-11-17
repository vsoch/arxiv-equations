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
yymm
Two digit year and month of items in the tar package. Starts with 9108 for 1991-08, rolls past y2k to 0001 for 2000-01, 1008 for 2010-08 etc.
```

Within the single folder, we have over 4000 files!

```bash
$ ls 0801 | wc -l
4516
```

## Testing Parsing

To test parsing and extraction of a .tar.gz within, please reference the script
[extractMetrics.py](extractMetrics.py).

**under development**

## Metrics of Interest 
