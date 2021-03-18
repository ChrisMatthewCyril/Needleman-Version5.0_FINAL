# Needleman
BIMM 143 Project

Goal: To be able to take two gene sequences from two different organisms, and be able to predict whether they are orthologs.

This project has two phases: a setup and a test.

socrates.py is the brain of this project. I've used biopython to write methods.
BenchmarkMaker.py is the setup phase.

LOGIC BEHIND THE SETUP PHASE:
I'm comparing seqs between humans and fruitflies. 
I have found 20 genes that have the same names and functions in both species.
I then compute the alignment scores between them, and adjust for length.
Average this ammong all 20 for a baseline reference. 

LOGIC BEHIND THE TEST PHASE:
Compute alignment between BMAL1 (human) and CYCLE (fruitfly)
Compare this alignment score with the baseline reference found in the above.
If it's within 5%, make the determination that they are orthologs (genes with different names, but same function)

Were we correct? Does this paradigm work? I hope so. Let's find out!