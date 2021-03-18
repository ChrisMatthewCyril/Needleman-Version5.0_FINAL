"""
    The socrates module is my toolbox. It uses BioPython's alignment module to compute alignment scores and do more.
"""
from Bio import SeqIO, Align
import os
import numpy as np

"""
Bio: BioPython module. Has a plethora of useful Bioinformatics tools. SeqIO helps me read seqs and align helps me align 
them.
OS: Lets me go through the computer's file directory and read data from the DataBank folder that you NEED!
numpy: Useful math functions.

"""


def __load_seq(link):
    """
    Internal method, Loads sequences from the file link
    :param link: File URL
    :return: Dictionary of format: "record id": sequence
    """
    records = {}
    for record in SeqIO.parse(link, "fasta"):
        records[record.id] = record.seq
    return records


def get_filenames(folder_link):
    """
    Fetches and organizes fasta files in a folder.
    :param folder_link: URL to the folder
    :return: alphabetically sorted human and fly gene files, that were found in the specified folder.
    """
    human_genes = []
    fly_genes = []
    for file in os.listdir(folder_link):
        if file[:2] == "HS":
            human_genes.append(file)
        elif file[:2] == "DM":
            fly_genes.append(file)
        else:
            continue

    return sorted(human_genes), sorted(fly_genes)


def get_first_id(record_dictionary):
    """
    Returns the first sequence from a dictionary of records.
    :param record_dictionary: Input dictionary
    :return: First key of the dictionary, which is the sequence ID of the first sequence in the fasta file.
    """
    return list(record_dictionary)[0]


def get_first_seq(file_path):
    """
    Gets the first sequence from a file path. Uses internal load_seq method.
    :param file_path: Duh.
    :return: The first sequence found in the fasta file.
    """
    record_dictionary = __load_seq(file_path)
    first_index = get_first_id(record_dictionary)
    return record_dictionary[first_index]


def compare_seqs(human_seq, fly_seq):
    """
    Computes the alignment score between a homo sapiens and a drosophila melanogaster sequence.
    Uses BioPython.Align.PairwiseAligner.
    Note: I claim that it uses Needleman-Wunsch, and indeed it does for all test cases.
    However, in practice, PairwiseAligner automatically chooses between 4 algorithms.
    You can find more information at: https://biopython.org/docs/1.75/api/Bio.Align.html?

    :param human_seq: The homo sapiens sequence.
    :param fly_seq: The drosophila melanogaster sequence.
    :return: Alignment score.
    """
    align_machine = Align.PairwiseAligner()
    align_machine.mode = 'global'
    alignment = align_machine.align(human_seq, fly_seq)
    print("Using " + align_machine.algorithm + " algorithm. Alignment score: ", alignment.score, "\n\n")
    return alignment.score


def average_score(score, human_seq, fly_seq):
    """
    Computes the average score between homo sapiens and drosophila melanogaster pairings.
    :param score: Array of Needleman-Wunsch scores.
    :param human_seq: Array of homo sapien sequences. (Yes, the loooong sequence is in here)
    :param fly_seq:  Array of drosophile melanogaster sequences.
    :return: Array of average scores, computed per pair.
    """

    average_array = []
    for a, b, c in zip(score, human_seq, fly_seq):
        average = a/((len(b)+len(c))/2)
        average_array.append(average)

    return average_array


def grand_average(input_array):
    """
    Returns average alignment score.
    :param input_array: A float array.
    :return: Average alignment score.
    """
    return np.average(input_array)


def find_average(score, human_seq, fly_seq):
    """
    Returns the length-normalized alignment score.
    :param score: Alignment score.
    :param human_seq: Human Sequence, string.
    :param fly_seq: Fly Sequence, string.
    :return: Length-normalized alignment score.
    """
    return score/((len(human_seq)+len(fly_seq))/2)

