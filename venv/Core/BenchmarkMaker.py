import Socrates as sc
import Recorder as rec

benchmark_average = 0 # This is the same thing as the "Gene Deviation Score."
"""
    This is the module that sets up the Benchmark average score standard. 
    All you have to do is call run_program(), and specify the file path to the folder of fasta files.
    Everything is automated.
    This relies on the Socrates module, using it as a toolbox.
"""


def run_program(repository):
    """
    This method parses the repository, extracting human and fly files as it does so. It then computes alignment
    scores between pairings, and deposits information into the Recorder for later use (plotting).
    It will then compute the average length-normalized alignment score. For more information, read the # comments below!
    :param repository: The filepath of the collection of human and fly fasta files.
    :return: nothing.
    """
    # Step 1 We need sequences! To save time, we'll keep the first sequence in each file. What are the files?
    human_files, fly_files = sc.get_filenames(repository)

    # Step 2 construct the full filepaths, and get the FIRST sequences only and store them in a dictionary.
    # Key = filename, Value = String seq.

    human_seqs_dict = {}
    fly_seqs_dict = {}

    # Getting seqs from the DataBank.
    for human_file, fly_file in zip(human_files, fly_files):
        human_seqs_dict[human_file] = sc.get_first_seq(repository + human_file)
        fly_seqs_dict[fly_file] = sc.get_first_seq(repository + fly_file)

    # At this stage, we have two dictionaries that should be in alphabetical order each, with filenames corresponding
    # to sequences.

    # The next step is to compute the needleman-wunsch score between them

    needle_scores = {}
    for human_key, fly_key in zip(human_seqs_dict, fly_seqs_dict):
        print("Computing alignment score between: " + human_key + " and " + fly_key)
        needle_scores[human_key + " vs " + fly_key] = sc.compare_seqs(human_seqs_dict[human_key],
                                                                      fly_seqs_dict[fly_key])
        # Now I'm recording this new addition!
        # This might get a little confusing so I'm gonna explain
        # The first statement below will give me data for a histogram.
        # The second statement computes the average length of the two seqs and passes it as well as the score
        rec.add_pair_score(human_key, fly_key, needle_scores[human_key + " vs " + fly_key])
        rec.add_length_data(len(human_seqs_dict[human_key]) + len(fly_seqs_dict[fly_key]) / 2,
                            needle_scores[human_key + " vs " + fly_key])

    # Now we need to compute the average normalized scores for each pairing
    average_per_pair = sc.average_score(list(needle_scores.values()), list(human_seqs_dict.values()),
                                        list(fly_seqs_dict.values()))

    # Now we need to compute the grand average
    global benchmark_average
    benchmark_average = sc.grand_average(average_per_pair)

    print("\nBenchmark Average Alignment Score: " + str(benchmark_average) + " points per base.")


# Helper method, returns average
def get_benchmark_average():
    """
    Returns the Gene Deviation Score.
    :return: Float, benchmark_average
    """
    return benchmark_average


# Helper method, sets the recorder's gene deviation score.
def record_benchmark_average():
    """
    Records the Gene Deviation Score into the recorder.
    :return: Nothing.
    """
    rec.set_gene_dev_score(benchmark_average)


# Helper method, returns the reference to the local recorder object.
def get_recorder_object():
    """
    Returns Recorder object reference.
    :return: Recorder object, 'rec'
    """
    return rec


class Benchmarker:
    pass
