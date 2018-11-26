# Can we predict domains of math from equations in the article?

For this analysis, we will use:

 - The [model](../statistics/models) derived from equations across 66K+ equations from statistics articles in Wikipedia
 - The [equations](../math) that are math domain specific.

For both of these tasks, we will use the script [equationAnalysis.py](equationAnalysis.py).
We look at both embeddings generated using single characters, and embeddings using LaTeX
symbols and remaining characters.
