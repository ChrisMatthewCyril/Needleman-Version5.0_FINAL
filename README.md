# Needleman
BIMM 143 Project

HOW TO RUN THIS: My recommendation is PyCharm. Please run the file "Decipher.py." Bear in mind that you'll have to provide the links to folders and files that the program requests. Super easy, please look at the images in the "guide" folder.  To copy the full filepath, use Shift+Command+C and don't forget your forward or backslashes! (Depends if you're using Windows or Mac OS)

Anyway... Goal: To be able to analyze two gene sequences from two different organisms, and be able to predict whether they are orthologs.

This project has two phases: a setup and a test.

MODULES Socrates.py is the brain of this project. I've used biopython to write its methods. BenchmarkMaker.py is the setup phase. Decipher.py is the file you should run. Recorder.py... records information! (surprise, surprise) :P ReporterTester.py is a misnomer, but it tests the Recorder file, it's a little embarassing, but feel free to take a look.

FOLDERS

Databank: Contains the sequences that will be used to construct the gene deviation score. BMAL_CYC_FILES: Contains the two BMAL and CYC sequences. These are KNOWN orthologs. I'm going to check if my program can validate that.

LOGIC BEHIND THE SETUP PHASE: I'm comparing seqs between humans and fruitflies. I have found 20 genes (10 pairs) that have the same names and functions in both species. I then compute the alignment scores between them, and adjust for length. Average this ammong all 20 for a baseline reference. 

LOGIC BEHIND THE TEST PHASE: Compute alignment between BMAL1 (human) and CYCLE (fruitfly) Compare this alignment score with the baseline reference found in the above. If it's within 5%, make the determination that they are orthologs (genes with different names, but same function)

Were we correct? Does this paradigm work? I hope so. Let's find out!

RESULTS: Printed in a PDF file! The link is in the console window!

# Introduction

## Scientific Question:
"Are BMAL1 and CYCLE orthologs?"

## Background:
During the course of evolution, phylogenetic splits occurred. These gave rise to the different kingdoms. Thus, we share a lot of common features with other species. For instance, consider the human hand and the flipper of a whale. Although a whale's flipper may very well be over 3 times the size of an entire human, the skeletal structure is extremely similar. Just bigger, and probably has a few bones fused together for strength, yet similar nonetheless. This suggests common ancestry.

It is no surprise then, that we also share many GENES with other animals and insects. Sometimes, scientists are lucky, and they find two genes with the same names and the same functions in two different species. Like the fruitfly, Drosophila Melanogaster and humans, Homo Sapiens. Scientists name genes according to their function. For instance, the CLOCK gene in the fruitfly was named because of its role in the circadian rhythm. CLOCK stands for: "circadian locomoter output cycles protein kaput." (1) BMAL1, whose official name is "aryl hydrocarbon receptor nuclear translocator like," was discovered animals. (2) It turns out that BMAL1 is involved in the circadian clock, and is very much alike to the CLOCK protein found in flies. (3)

Today, biologists know that CLOCK and BMAL1 are essentially the same genes, and both bind to CYCLE to form a heterodimer that controls the circadian clock.

BMAL1 and CLOCK are called orthologs. They have different names, but the same function, in two different species.

This begs the question: "Are there other orthologs like BMAL1 and CLOCK?" the answer is obviously yes! How useful would an algorithm that could predict orthologs be? Very! This can accelerate progress in genetics, which will directly benefit us in the pursuit of curing diseases. This is my goal with the current program: to use a reference number to predict whether two genes are orthologs.

I used (5) as a source list of human genes, then used my intution to guess which ones would have fly counterparts. (More information in the Analysis section below)

## Where is the data from? 
Using my intuition, I then pulled 10 pairs of genes from the NBCI's gene database at https://www.ncbi.nlm.nih.gov/gene/ – human, and fly. These genes have the same names, and are known to have the same functions. I compute the alignment scores between each pairing, normalize them for length, then average all these length-normalized scores to arrive at the "Gene Deviation Score."

This is the "gold standard." 

I know that BMAL1 and CYCLE are orthologs, as described above. I compute a length-normalized needleman-wunsch alignment score for this pairing, then check to make sure that it is within 5% fo the Gene Deviation Score I computed above.
See analysis for more!


## Scientific Hypothesis:
"If the alignment score between BMAL1 and CYCLE is within 5% of the gene deviation score, then they are orthologs according to my bioinformatics model."

## Analyses and How Data was Downloaded:
Only one analysis was performed: A needleman-wunsch alignment. The result were plotted in two forms:
1. Bar Chart, displaying the relationship between the human and fly sequence pairings and the length-normalized alignment score.
2. Line Chart, displaying the relationship between the average length of the pairings and the alignment score.

Data was downloaded from the NCBI's repository under the search type "GENE." 
For example, I pulled the BMAL1 file from: "https://www.ncbi.nlm.nih.gov/gene/406" by clicking on the fasta button on the webpage.
This process was repeated for every gene found, with care taken to ensure that it was from the right species.

## What is the Needleman-Wunsch Algorithm?
A sequence alignment algorithm, that computes the best alignment score between two sequences. It penalizes mismatches and gaps in the sequence, as you shall see below.

Setup:
Form a matrix, filling in the first row and column with '-1' Then, fill in one row per base of the first sequence, and one column per base of the second sequence.

Scoring:
Match: +1
Mismatch: -1
Gap: -2

Protocol:
1. Fill in multiples of -2 for the first row and the first column. (Gap Penalty)
2. Begin working through the sequence. For each cell, the score is the highest of the following:
	a) Top left diagonal + match or mismatch score
	b) Left cell's score - 2
	c) Top cell's score - 2
3. Draw an arrow pointing from the cell used in step (2) toward your current cell.
4. Repeat for every character in sequence.
5. To find the best alignment, begin at the highest score found on the bottom right corner of the matrix, and follow the arrows backwards, tracing around the next highest score. This is the likely sequence alignment.

All information from: (4) below.

In practice, BioPython, a collection of BioInformatics methods for the Python programming language, uses a Needleman-Wunsch score alignment algorithm.
This program uses the Pairwise Aligner, from Bio.Align. (6) Since the pairwise aligner automatically chooses the best algorithm to compute the alignment, I make it print out
which one it' using. In this project, it stuck to the Needleman-Wunsch algorithm.

## Analyses:
1. Bar chart, plotting the length-normalized needleman wunsch alignment score for the different pairings.
2. Line chart, plotting the relationship between average pairing length, i.e., human gene length and fly gene length average, vs. raw needleman-wunsch alignment score.
3. Table, with ength-normalized needleman wunsch alignment score for the different pairings.
## References:
1. https://www.ncbi.nlm.nih.gov/gene?Db=gene&Cmd=DetailsSearch&Term=9575
2. https://www.ncbi.nlm.nih.gov/gene?Db=gene&Cmd=DetailsSearch&Term=406
3. "Mammalian Clock 20201103.rec.pdf" Susan Golden and Michael Goldman, BIMM 116 FALL 2020. I took this class last quarter! Still remember quite a few details.
4. 'Video: From Dot Plots to BLAST' Jamie Schiffer. https://canvas.ucsd.edu/courses/24319/assignments/250086?module_item_id=662582
5. https://genomics.senescence.info/genes/allgenes.php
6. https://biopython.org/docs/1.75/api/Bio.Align.html

NCBI = National Center for Biotechnology Information.

# Section 2: Loading Packages

Please see comments in code, located at venv/Core/.

# Section 3: Performing Bioinformatics Analysis

This code works extensively with the data type: .fasta

Directly quoting the NCBI, "A sequence in FASTA format begins with a single-line description, followed by lines of sequence data. The description line (defline) is distinguished from the sequence data by a greater-than (">") symbol at the beginning. It is recommended that all lines of text be shorter than 80 characters in length." (1)

Simply put, it is a text file with sequences. Importantly, there might be multiple sequences of the same gene withing a file. Due to limitations on computing power, and for the sake of time, I've chosen to use the first sequence of each file. 

## What is the Needleman Wunsch Algorithm?
A sequence alignment algorithm, that computes the best alignment score between two sequences. It penalizes mismatches and gaps in the sequence, as you shall see below.

Setup:
Form a matrix, filling in the first row and column with '-1' Then, fill in one row per base of the first sequence, and one column per base of the second sequence.

Scoring:
Match: +1
Mismatch: -1
Gap: -2

Protocol:
1. Fill in multiples of -2 for the first row and the first column. (Gap Penalty)
2. Begin working through the sequence. For each cell, the score is the highest of the following:
	a) Top left diagonal + match or mismatch score
	b) Left cell's score - 2
	c) Top cell's score - 2
3. Draw an arrow pointing from the cell used in step (2) toward your current cell.
4. Repeat for every character in sequence.
5. To find the best alignment, begin at the highest score found on the bottom right corner of the matrix, and follow the arrows backwards, tracing around the next highest score. This is the likely sequence alignment.

All information from: (2) below.

In practice, BioPython, a collection of BioInformatics methods for the Python programming language, uses a Needleman-Wunsch score alignment algorithm.

## References:
1. https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=BlastHelp
2. 'Video: From Dot Plots to BLAST' Jamie Schiffer. https://canvas.ucsd.edu/courses/24319/assignments/250086?module_item_id=662582


# Section 4: Plotting the results

## Data Analysis Method:
After computing the following:

(1) Needleman-Wunsch Alignment Score
(2) Length-normalized version of (1)

The following were constructed:

(1) A Bar Chart
	This displays the length-normalized needleman-wunsch scores for the different pairings of human vs. fly genes.
(2) A Line Chart
	This displays the relationship between average pairing length and needleman-wunsch alignment score. I expect that longer sequences will show greater alignment scores, given that I already know that these genes are the same between the fruitly and the human. 
(3) A Table
	Displaying length normalized needleman-wunsch scores correspnding to each pairing. 

In order to make the results accessible, I used FPDF to construct a PDF file with vital information, which includes a link to the GitHub page where you can find my code.
The two charts above are stored in a folder of your choosing.

I highly recommend checking the comments found in the file venv/Core/Recorder.py to follow along the code for a better understanding.

# Section 5: Analysis

I know the truth – BMAL1 and CYCLE are orthologs. However, my program does not catch this. I have identified a few reasons why. 

First, realize that I've only used ten gene pairs, there are hundreds of similar genes between fruitflies and humans. I believe that increasing the number of samples would improve the prediction. In order to do so, I need a database that can automatically compile a .zip file with gene pairings between fruitflies and humans. In my case, I had to use a list of human genes, which you can find at (2) below. Looking through the list, I began to recognize some names. I was able to use my intuition to guess which ones were SUPER essential to life, and correctly deduced that they would, by neccessity, have fly paralogs. Combining this intuition with my knowledge of common genes that I've seen in biology classes before, I compiled the list of ten gene pairs from the NCBI's database, as mentioned in the introduction above.

Second, within each fasta file is a collection of 5 or more sequences. I wanted to analyze pairings between each of the sequences. Unfortunately, that would take a very long time with the computers we have, so I didn't. But ideally, I would compare individual sequence alignments to determine the best fit, and use that value for the remainder of the code.

Third, take a look at the math. I compute a score, divide it by the AVERAGE length of the sequences, then sum all such averages and take ANOTHER average. When I take multiple averages, I'm allowing the computation to be susceptible to outliers. I think there might be a better way to find "common ground," without suffering from the consequences of averages. 

Fourth, my tolerance of 5% might have been too harsh considering the limited data I have to work with. Increasing it to 15, 20 or even 40% might have made a difference, but then again, increasing the tolerance comes at the cost of reduced accuracy. Moreover, increasing the tolerance too high defeats the whole purpose of this algorithm, because now the bar to be considered an ortholog is very low, and I can expect more errors to stem from the increase. 5% is the accepted range even in the statistical community, and I believe that changing it is folly.
           
My proposed solution would be to sample more genes, find better alignments by going through each sequence that we have, then separate them into length-based clusters, since it is possible that gene length plays a critical role in the accuracy of my results. The prediction tool can then first compute sequence lengths and apply a more customized algorithm which takes into account the length of the gene, and I hope that this will be better at predicting whether two genes are orthologs, or not!

## References for this section:
(1) My brain :P
(2)https://genomics.senescence.info/genes/allgenes.php

Thank you for reading! :D
