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

# File paths below.
DataBank_source = ""
report_filename = ""
report_dest = ""
BMAL_filepath = ""
CYC_filepath = ""
final_destination = ""

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
    pdf.write(h=1, txt="\nGitHub Link To Code", link="https://github.com/ChrisMatthewCyril/Needleman/tree/Version3.0")
    pdf.set_text_color(0, 0, 0)

    pdf.write(h=1, txt="\nCalculated Gene Deviation Score: " + str(gene_deviation_score))
    pdf.write(h=1, txt="\n Number of Gene pairs: " + str(num_pairs))
    pdf.add_page(orientation="P")

    pdf.set_font('Arial', style='B')
    pdf.cell(w=14, h=1, txt="Compared Files", border=1, ln=0, align='L', fill=False)
    pdf.cell(w=6, h=1, txt="Needleman-Wunsch Score", border=1, ln=1, align='L', fill=False)
    pdf.set_font('Arial', style='')

    # Making table of gene pairings with alignment scores.
    for first_file, second_file in gene_pair_scores:
        pdf.cell(w=14, h=1, txt=first_file + " vs " + second_file, border=1, ln=0,
                 align='L', fill=False)
        pdf.cell(w=6, h=1, txt=str(gene_pair_scores[(first_file, second_file)]), border=1, ln=1, align='R', fill=False)

    # Making bar and line charts.

    barchart_path = plot_bar()
    linechart_path = plot_line()

    # Adding the bar and line chart images from their links on the computer.
    pdf.add_page(orientation='landscape')
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
          "Don't forget to pick up your report! You can find it at: " + str(pdf_location))


# Plots a bar chart, shows up on the console. Also saves the figure to the user-specified directory. Returns path.
def plot_bar():
    """
    Plots a high-resolution bar chart of the different pairings and the length-normalized alignment scores.
    :return: Filepath of the bar chart.
    """
    name_list = [tuple[0] + "\n vs \n" + tuple[1] for tuple in gene_pair_scores.keys()]
    py.bar(name_list, gene_pair_scores.values())
    py.xticks(fontsize=8)
    py.ylabel("Needleman-Wunsch Length Normalized Score")
    py.title("Comparison Pairings vs Length-Normalized Scores")
    global final_destination
    filename = final_destination / "BarChart.jpg"
    print("Please wait, generating high-resolution bar chart...")
    py.savefig(filename, dpi=4500, orientation='landscape')
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
    filename = final_destination / "LineChart.jpg"
    sorted_list = collections.OrderedDict(sorted(gene_len_score.items()))
    py.plot(sorted_list.keys(), sorted_list.values())
    py.xlabel("Average Length of Pairings (bases)")
    py.ylabel("Needleman-Wunsch Length Normalized Score")
    py.title("Average Length of Pairings vs Length-Normalized Scores")
    print("Please wait, generating high-resolution line chart...")
    py.savefig(filename, dpi=4500, orientation='landscape')
    print("Done.\n")
    py.show()

    return str(filename)
