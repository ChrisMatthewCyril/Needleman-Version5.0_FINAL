import Socrates as sc
import BenchmarkMaker as bm
'''
Socrates is BioPython-based. It gives me the tools I need to execute my algorithm.
BenchmarkMaker is another model I created. It sets up the "Gene Deviation Score."
'''

# Receiving all user input: Destination FilePath, Destination FileName, DataBank location, BMAL and CYCLE locations.
report_filepath = input("Enter the full filepath where you'd like the report to go (Don't forget the final slash! (\\ or"
                        " / depending on your operating system): ")
filename = input("Pick a name for the report: ")
bmal_filepath = input("Enter the full filepath of the BMAL1 fasta file:")
cycle_filepath = input("Enter the full filepath of the CYCLE fasta file:")
DataBank_source = input("Enter the full filepath of the DataBank folder provided  (Don't forget the final slash!) :")
print("\n")

########################################################################################################################
########################################################################################################################

# First, I'm passing the databank path to benchmarkmaker to make the standard.
# Since benchmark maker has a recorder object, I wish to use the same one. So I get the reference from benchmark maker.
# Then I get the standard from benchmarkmaker the "gene deviation score."
# I pass this to recorder for logging purposes. I could've done this in a single step, but I wanted to make it clear to
# you. :)
bm.run_program(DataBank_source)
recorder = bm.get_recorder_object()
standard = bm.get_benchmark_average()
recorder.gene_deviation_score = standard


########################################################################################################################
########################################################################################################################
########################################################################################################################
# RECORDING THE FILE PATHS FOR THE FINAL REPORT. I'm passing the information onto the recorder. Look at the recorder
# module for more sense.

recorder.report_dest = report_filepath
recorder.report_filename = filename
recorder.source_path = DataBank_source
recorder.BMAL_filepath = bmal_filepath
recorder.CYC_filepath = cycle_filepath

########################################################################################################################
########################################################################################################################
########################################################################################################################

# Get BMAL and CYCLE sequences. These are known to be orthologs.
bmal1_seq = sc.get_first_seq(bmal_filepath)
cycle_seq = sc.get_first_seq(cycle_filepath)

# Compare sequences and get alignment score.
score = sc.compare_seqs(bmal1_seq, cycle_seq)

# Normalize it for the length.
average_score = sc.find_average(score, bmal1_seq, cycle_seq)
recorder.bmal_vs_cycle = average_score

# Check if the calculated length is within 5% of the goal standard.
if standard-(0.05 * standard) >= average_score >= standard+(0.05 * standard):
    print("According to the program, BMAL1 and CYCLE are orthologs.\n Writing Report...")
    # Tells recorder that the program has also determined the truth.
    recorder.calculated_true_correlation = True

else:
    print("BMAL1 and CYCLE are orthologs, but NOT according to the program. Writing Report...")

# Invokes the recorder, telling it to prepare a project report.
recorder.prepare_report()

