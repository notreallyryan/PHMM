# PHMM

In biological studies, proteins are often classified into different evolutionary families. Proteins in the same family share a common function and by extension, have similar amino acid sequences. 
As such, classifying a protein early is useful in the field, as it narrows down the characteristics of the protein, reducing the time and finances needed for lab work. While classification inevitably requires 
some lab work in order to confirm a protein's family, computational techniques can provide a good estimate of where to start.

The most basic protein family classification is accomplished by using Supervised Machine learning and Profile Hidden Markov Models. In this project, models are generated from multiple aligned amino acid sequences within the same family, and a modified version of the Forwards Algorithm is used to find which model best matches a queried sequence.  

## Instructions for Use

**Requires numpy and pandas to use

1. For each protein family you want to model, put one .fasta file in the FASTA folder. the .fasta file should contain all the aligned sequences that make up that family. (ie. each sequence must be the same length.)
2. For each queried sequence, put a fasta file in the QUERIED folder.
3. Run the program by...

   
