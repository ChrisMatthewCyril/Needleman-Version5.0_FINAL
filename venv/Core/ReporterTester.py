import Recorder as rec
from random import randint

'''
-NOT TO BE USED! Filepaths and nonsense are hard coded here for testing purposes.

This is a tester that I used to test the recorder module. 
Recorder is my custom module that writes out to a PDF file.
Random was used to generate nonsense data for testing purposes.
Oooo weee, this was fun! 
'''

# Setting filepaths/names.
rec.report_dest = "/Users/chrismatthewcyril/Downloads/GeneBank/Needleman-Version5.0/venv/"
rec.report_filename = "1"
rec.BMAL_filepath = "/Users/chrismatthewcyril/Downloads/GeneBank/Needleman-Version5.0/venv/BMAL_CYC_FILES/BMAL.fasta"
rec.CYC_filepath = "/Users/chrismatthewcyril/Downloads/GeneBank/Needleman-Version5.0/venv/BMAL_CYC_FILES/CYCLE.fasta"
rec.DataBank_source = "/Users/chrismatthewcyril/Downloads/GeneBank/Needleman-Version5.0/venv/DataBank"

# Testing out the add_pair_score function, as well as feeding nonsense data.
rec.add_pair_score("bmal", "cycle", 2000)
rec.add_pair_score("askdfj", "aslkdj", 1500)
rec.add_pair_score("asd", "123", 500)
rec.add_pair_score("adlkjhads", "123", 12)
rec.add_pair_score("bmajskndsaal", "cycle", 250)

for x in range(50):
    rec.add_length_data(x, randint(1,2500))

# Asking for report to check it.
rec.prepare_report()