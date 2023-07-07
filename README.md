# Predicting Protein Families using Profile Hidden Markov Models

In biological studies, proteins are often classified into different evolutionary families. Proteins in the same family share a common function and by extension, have similar amino acid sequences. 
As such, classifying a protein early is useful in the field, as it narrows down the characteristics of the protein, reducing the time and finances needed for lab work. While classification inevitably requires 
some lab work in order to confirm a protein's family, computational techniques can provide a good estimate of where to start.

The most basic protein family classification is accomplished by using Supervised Machine learning and Profile Hidden Markov Models. In this project, models are generated from multiple aligned amino acid sequences within the same family, and a version of the Forwards Algorithm is used to find which model best matches a queried sequence.  

## Instructions for Use

_Requires numpy and pandas to use_

1. For each protein family you want to model, put one .fasta file in the FASTA folder. the .fasta file should contain all the aligned sequences that make up that family. (ie. each sequence must be the same length.)
2. For each queried sequence, put a fasta file in the QUERIED folder.
3. Run the program by running main.py, and following the prompts given

## How it works

### Making the Profile Hidden Markov Models

Assuming that the sequences provided are already aligned, the first step is to find which sequence indices are likely to be "key features" of the family. This can be done by observing the number of blanks at that index.
If more sequences have blanks at that particular location, the amino acids observed at that location are more likely to be insertions than hallmark traits. Conversely, blanks at locations with many observed amino acids are likely to be deletions.

![image](https://github.com/notreallyryan/PHMM/assets/96549151/28cfbc20-37f2-4a60-ade7-c8a4403668a4)

In this implementation, the user set a value that the fraction of observed amino acids must exceed to be considered a key feature. (ie a value of 0.5 means at least half of the observations at an index must be amino acids to be a key feature) This allows the user to control how flexible a model is. A smaller fraction will increase the matchability between model and any arbitrary sequence, while a larger one will cause the model to be more specific to the family. 

The second step is to generate the appropriate nodes and connections for the model. In this implementation, Match and Delete Nodes connect to the next Match, Delete, and Insert Node, while Insert Nodes connect to the next Match and Delete Node, but also to themselves. This accounts for the possibility of multiple consecutive inserts between key features. A Start and an End Node are added for simplicity.

![image](https://github.com/notreallyryan/PHMM/assets/96549151/778fab06-936e-4d52-8ad6-408631d94a4b)

The last step is to add the transition and emission probabilities to each node, making sure to use the lapalcian smoothing trick, giving each node two sets of probabilities. 

_Note: Steps 1, 2, and 3 are done simultaneously in this implementation so that each model only requires one pass through_ <br />
_Additional Note: The use of objects as Nodes allows for better envisioning of the model. However, the same model could be achieved using a single 2D array._

### The Forwards Algorithm

In order to determine which model the unknown sequence best matches, the Forward Algorithm can be used to find the probability of a model generating a given sequence. By comparing these probabilities, the best fitting model can be isolated.

The basics and mathematical derivation of the algorithm can be found [here](https://en.wikipedia.org/wiki/Forward_algorithm), but essentially the algorithm uses the probabilities of being in a prior state with the emission and transition probabilities to calculate the probability of arriving at the current state. The probability sum across all of the states in the last timestep is the probability that the model produces the given sequence.

For Profile Hidden Markov Model, the algorithm is changed slightly. Instead of basing the current probability off the probability of being in the last state, the calculation takes into account the probability of the previous recorded amino acid being at a previous state.

So for each node in the model, the algorithm must compute the probability of each of the amino acids in the sequence being at that node. Those values can then be used to calculate the new values in the next iteration of the Forwards Algorithm

For Match Node at position _x_, the probability of an amino acid _y_ being expressed by this node relies on the probability of amino acid _y-1_ being expressed by Match and Insert node _x-1_ (M_{x-1}(_y-1_) and I_{x-1}(_y-1_)) and the probability that the amino acid supposed to be at position _y_ was deleted (D_{x}(_y_))

For a Del Node at the same position, the calculation of whether a deletion occured between _y-1_ and _y_ relies on whether the previous amino acid _y-1_ was expressed by the previous Match and Insert Nodes (M_{x-1}(_y-1_) and I_{x-1}(_y-1_)), as well as whether there were any other amino acids supposed to be at position _y_ that were deleted (D_{x-1}(_y_))

Insert Nodes at position _x_ depend on M_x and D_x. For a calculation regarding amino acid _y_ in I_x, the algorithm requires input from M_x(_y-1_) and D_x(_y_). It also requires input from itself, as whether amino acid _y_ is an insert depends on whether amino acid _y-1_ was an insert (I_x{_y-1_}

