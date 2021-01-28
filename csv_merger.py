import pandas as pd
import sys

# Author: Edwin Lim (Director of TechOps)
# Date: January 28, 2021
#
# This is a python script that merges emails from different .csv
# files together, getting rid of duplicates. Instructions for use
# can be found at [insert wiki link].
#
# We require an even number of arguments for this script:
# (filename)  A name of the .csv file to be merged
# (colname)   Name of the column that contains email addresses for the .csv file just given
#
# Usage: python3 webscraper_script.py (filename) (colname) ... (as many filename/colname pairs necessary)
num_arguments = len(sys.argv) - 1
if num_arguments % 2 != 0:
    print("We require an even number of arguments.")
    print("Please check [insert wiki link] for instructions on how to use this script.")
    exit()

# Dictionary uses hashing to avoid redundant email entries
unique_emails = {}

# Checking validity of arguments and merging results if valid
for i in range(1, num_arguments + 1, 2):
    filename = sys.argv[i]
    colname = sys.argv[i + 1]
    csv_file = pd.read_csv(filename)

    if not colname in csv_file:
        print("Column " + colname + " does not exist in " + filename)
        exit()

    emails = csv_file[colname]
    for email in emails:
        if email in unique_emails.keys():
            unique_emails[email] = unique_emails[email] + 1
        else:
            unique_emails[email] = 1

# Creating a .csv file consisting of all unique email addresses
all_emails = pd.DataFrame(unique_emails.keys(), columns = ['email'])
all_emails.to_csv('all_emails.csv')