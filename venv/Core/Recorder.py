import os
import collections

from fpdf import FPDF
import datetime
from matplotlib import pyplot as py
from pathlib import Path

'''

Package Definitions:

os: Operating system-related functions. I ues it to create a directory in your computer and store my report.
collections: This helps me create a sorted dictionary later on below. Has a plethora of functions related to grouping
like tuple, lists, dictionaries etc.
datetime: For time and date related functions. 
fpdf: Enables me to make a PDF, attach matplotlib plots and more!
matplotlib, pyplot: I can make bar and line graphs!
pathlib: Helps me deal with paths regardless of operating systems. There are different conventions and this makes it 
easy.
'''

# User-defined file paths below.
"""
Databank_source: The filepath of the databank folder. This contains the reference sequences.
report_filename: User-defined report name.
report_dest: User-defined report destination. Note, all graphs will be deposited here.
BMAL_filepath: Location of BMAL1 .fasta file.
CYCLE_filepath: Location of CYCLE .fasta file.
final_destination: a string for internal use, used to create directory in prepare_report() method
"""
DataBank_source = ""
report_filename = ""
report_dest = ""
BMAL_filepath = ""
CYC_filepath = ""
final_destination = ""

"""
gene_pair_scores: Dictionary to hold pairing names and scores.
gene_len_score: Dictionary to hold pairing lengths and scores.
Other variable functions may be inferred as per name.
"""
# Arrays below hold information for plotting later on. The variables are simply initialized.
gene_pair_scores = {}
gene_len_score = {}
num_pairs = 0
gene_deviation_score = 0
calculated_true_correlation = False
bmal_vs_cycle = 0


# Adds a pair with alignment score to the gene_pair_scores dictionary. Also upps the count of num pairs by 1. This will
# be used for the report later on.
def add_pair_score(filename1, filename2, score):
    """
    Logs a length-normalized score for a given pairing. For use in the bar chart below.
    :param filename1: Human filename
    :param filename2: Fly filename
    :param score: Length Normalized Needleman-Wunsch alignment score.
    :return:
    """
    gene_pair_scores[(filename1, filename2)] = score
    global num_pairs
    num_pairs += 1


# This will be used to plot length vs. score later on in the code. Adds to the gene_len_score list for later use.
def add_length_data(average_length, score):
    """
    Appends average length between fly and human seq, with corresponding score.
    :param average_length: The average length between a fly and human gene.
    :param score: Needleman-Wunsch score.
    :return: Nothing.
    """
    gene_len_score[average_length] = score


# Prepares Report, opens pdf file at user-selected destination.
def prepare_report():
    """
    Master method, creates a folder with the user's desired filename, and writes a PDF report with salient information.
    Also creates a line chart and a bar chart!
    :return: Nothing.
    """
    # Get list of folders in user's desired directory. Check to make sure that they entered valid information.
    try:
        local_list = os.listdir(report_dest)
    except NotADirectoryError:
        print("Wrong Directory Specification.")
        quit()

    # Setting final destination of the report.
    global final_destination
    final_destination = Path(report_dest + "REPORT/")
    # Checking to make sure that we are able to create a folder at the user's desired filepath.
    # If invalid, program quits.
    if local_list.count("REPORT") == 0:
        try:
            os.mkdir(final_destination)
        except FileNotFoundError:
            print("Incorrect filepath.")
            quit()

    # Begin writing to PDF.
    pdf = FPDF(orientation="P", unit='cm', format="Letter")
    pdf.set_font('Arial')
    pdf.set_author("Chris Matthew Cyril")
    pdf.set_font_size(12)
    pdf.add_page(orientation="P")
    pdf.set_title(title="REPORT")
    pdf.write(h=0, txt='GENERATED REPORT -- ' + str(datetime.datetime.now()))
    pdf.write(h=1, txt="\nDataBank source was found in: " + DataBank_source)
    pdf.write(h=1, txt="\nBMAL Filepath: " + BMAL_filepath)
    pdf.write(h=1, txt="\nCYCLE Filepath: " + CYC_filepath)
    pdf.write(h=1, txt="\nThis report can be found at: " + str(final_destination))
    pdf.set_text_color(0, 255, 255)
    pdf.write(h=1, txt="\nGitHub Link To Code", link="https://github.com/ChrisMatthewCyril/Needleman-Version5.0_FINAL/tree/Version5.1")
    pdf.set_text_color(0, 0, 0)

    # Writing Gene Deviation score and number of gene pairs used.
    pdf.write(h=1, txt="\nCalculated Gene Deviation Score: " + str(gene_deviation_score))
    pdf.write(h=1, txt="\n Number of Gene pairs: " + str(num_pairs))
    pdf.add_page(orientation="landscape")

    # Begin table of gene pairings with alignment scores.
    pdf.set_font('Arial', style='B')
    pdf.cell(w=14, h=1, txt="Compared Files", border=1, ln=0, align='L', fill=False)
    pdf.cell(w=6, h=1, txt="Length Normalized Score", border=1, ln=0, align='L', fill=False)
    pdf.cell(w=6, h=1, txt="Group Code for Bar Chart", border=1, ln=1, align='L', fill=False)
    pdf.set_font('Arial', style='')


    # Making a G-list, groupings, so you can refer to this as a key for the Bar Chart. Counter initialized to 0
    g_list = ["G"+str(x) for x in range(1, num_pairs+1)]
    count = 0
    # Making table of gene pairings with alignment scores.
    for first_file, second_file in gene_pair_scores:
        pdf.cell(w=14, h=1, txt=first_file + " vs " + second_file, border=1, ln=0,
                 align='L', fill=False)
        pdf.cell(w=6, h=1, txt=str(gene_pair_scores[(first_file, second_file)]), border=1, ln=0, align='L', fill=False)
        pdf.cell(w=6, h=1, txt=g_list[count], border=1, ln=1, align='L', fill=False)
        count += 1

    # Making bar and line charts.

    barchart_path = plot_bar()
    linechart_path = plot_line()

    # Adding the bar and line chart images from their links on the computer.
    pdf.image(barchart_path, h=20, w=27)
    pdf.image(linechart_path, h=20, w=27)
    pdf.add_page(orientation='portrait')
    pdf.write(h=1, txt="Thanks for an amazing quarter, Professor Schiffer and the TA's!\n"
                       "Best, as always,\nChris Matthew Cyril :)")
    pdf.add_page(orientation='portrait')
#    pdf.write(h=1, txt=getAnalysis())
    pdf_location = final_destination / report_filename
    pdf.output(str(pdf_location) + ".pdf", dest='F').encode('latin-1')

    # Thank you! Close-out message.
    print("Thanks for an amazing quarter, Professor Schiffer and the TA's!\n"
          "Best, as always,\nChris Matthew Cyril :) \n"
          "Don't forget to pick up your report! You can find it at: " + str(pdf_location) + ".pdf")


# Plots a bar chart, shows up on the console. Also saves the figure to the user-specified directory. Returns path.
def plot_bar():
    """
    Plots a high-resolution bar chart of the different pairings and the length-normalized alignment scores.
    :return: Filepath of the bar chart.
    """
    # Generate group names for use in bar chart. Plot with length-normalized scores.
    py.bar([("G"+str(x)) for x in range(1, num_pairs+1)], gene_pair_scores.values())

    # Title and labels.
    py.ylabel("Needleman-Wunsch Length Normalized Score")
    py.title("Comparison Pairings vs Length-Normalized Scores")
    global final_destination
    filename = final_destination / "BarChart.jpg"
    print("Please wait, generating high-resolution bar chart...") # Print status message to console,

    # Save image                                                  # so user knows what's going on.
    py.savefig(filename, dpi=4500, orientation='landscape') # Save file.
    print("Done.\n")
    py.show()
    return str(filename)


# Plots a line chart, shows up on the console. Also saves the figure to the user-specified directory. Returns path.
def plot_line():
    """
    Plots a high-resolution line chart,  average length of pairings vs. Needleman-Wunsch length-normalized score.
    :return: Filepath of the line chart.
    """
    global final_destination
    filename = final_destination / "LineChart.jpg" # set destination
    sorted_list = collections.OrderedDict(sorted(gene_len_score.items())) # sort list for orderly line chart
    py.plot(sorted_list.keys(), sorted_list.values()) # plot line chart (x vs y)

    # Labeling below
    py.xlabel("Average Length of Pairings (bases)")
    py.ylabel("Needleman-Wunsch RAW Score")
    py.title("Average Length of Pairings vs Length-Normalized Scores")

    # Print status message to console, to user knows what's going on.
    print("Please wait, generating high-resolution line chart...")
    # Save line chart to user-defined directory.
    py.savefig(filename, dpi=4500, orientation='landscape')
    print("Done.\n")
    # Display line chart to console window.
    py.show()

    return str(filename)
