# Can we predict domains of math from equations in the article?

For this analysis, we will use:

 - The [model](../statistics/models) derived from equations across 66K+ equations from statistics articles in Wikipedia
 - The [equations](../math) that are math domain specific.

For both of these tasks, we will use the script [equationAnalysis.py](equationAnalysis.py).



## 1. Map Equations to Embedding Space

I had two choices now. I could either take the average of some set of equation vectors that I derived for
a topic, **or** work in a space with all the vectors (and labels to describe multiple cases of the same topic).
I decided to work with all the vectors and labels because taking some kind of average could dilute the signal.
The following steps are done in the script [2.generateEmbeddings.py](2.generateEmbeddings.py).

### Are equations from the same topic similar?
As a first sanity check, I'd want to see that equations from the same topic are similar, meaning
that their topics cluster together. So I did the following:

 - Start with character embeddings that are derived across entire set of equations, across all topics
 - For each topic, for each equation, map it to the space by generating it's vector (an average of it's character embeddings present in the model)
 - Now we have a vector representation (the same length, 300) for every equation!
 - Do clustering of the equation vectors, and (sanity check) the similar labels should cluster together (in progress)

I might go back at this point and choose more specific labels for kinds of math, as opposed to the statistics articles list that I chose. When there is a model that seems to be reasonably good, then I can do the same thing, but for equations in archive. For each paper in archive, I can again map the equations it includes to this space, and determine it's
"math topics" signature. These proportions can help us determine the domains of math that are highest priority for
penrose, and it's also just a really cool and interesting question anyway! 
