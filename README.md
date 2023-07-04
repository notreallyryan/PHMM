# PHMM

In biological studies, proteins are often classified into different evolutionary families. Proteins in the same family share a common function and by extension, have similar amino acid sequences. 
As such, classifying a protein early is useful in the field, as it narrows down the characteristics of the protein, reducing the time and finances needed for lab work. While classification inevitably requires 
some lab work in order to confirm a protein's family, computational techniques can provide a good estimate of where to start.

The most basic protein family classification is accomplished by using Supervised Machine learning and Profile Hidden Markov Models. In this project, models are generated from multiple aligned amino acid sequences within the same family, and a modified version of the Forwards Algorithm is used to find which model best matches a queried sequence.  

## Instructions for Use

_Requires numpy and pandas to use_

1. For each protein family you want to model, put one .fasta file in the FASTA folder. the .fasta file should contain all the aligned sequences that make up that family. (ie. each sequence must be the same length.)
2. For each queried sequence, put a fasta file in the QUERIED folder.
3. Run the program by...

## How it works

### Making the Profile Hidden Markov Models

Assuming that the sequences provided are already aligned, the first step is to find which sequence indices are likely to be "key features" of the family. This can be done by observing the number of blanks at that index.
If more sequences have blanks at that particular location, the amino acids observed at that location are more likely to be insertions than hallmark traits. Conversely, blanks at locations with many observed amino acids are likely to be deletions.

[add image later]

In this implementation, the user set a value that the fraction of observed amino acids must exceed to be considered a key feature. (ie a value of 0.5 means at least half of the observations at an index must be amino acids to be a key feature) This allows the user to control how flexible a model is. A smaller fraction will increase the matchability between model and any arbitrary sequence, while a larger one will cause the model to be more speciic to the family. 

The second step is to generate the appropriate nodes and connections for the model. In this implementation, Match and Delete Nodes connect to the next Match, Delete, and Insert Node, while Insert Nodes connect to the next Match and Delete Node, but also to themselves. This accounts for the possibility of multiple consecutive insertes between key features. A Start and an End Node are added for simplicity.

[add image later]

The last step is to add the transition and emission probabilities to each node, making sure to use the lapalcian smoothing trick.

[add image later]

_Note: Steps 1, 2, and 3 are done simultaneously in this implementation so that each model only requires one pass through_
_Additional Note: The use of objects as Nodes allows for better envisioning of the model. However, the same model could be achieved using a single 2D array._

### The Modified Forwards Algorithm

