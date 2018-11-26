library(pheatmap)

sim = read.csv("../vectors/similarity_character_math_embeddings.tsv",sep="\t",head=TRUE,stringsAsFactors=FALSE,row.names=1)
sim[is.na(sim)] = 0
sim[is.null(sim)] = 0

# Just plot as is
pdf("similarity_math_embeddings.pdf",width=50,height=50)
pheatmap(sim,title="Wikipedia Math Embedding Similarity")
dev.off()
