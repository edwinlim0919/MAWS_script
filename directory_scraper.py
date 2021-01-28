import pandas as pd
import time
import requests
import sys
from bs4 import BeautifulSoup

# Author: Edwin Lim (Director of TechOps)
# Date: January 27, 2021
#
# This is a python script that scrapes the Cal Directory to find 
# what emails belong to graduated students. Instructions for use can 
# be found at [insert wiki link].
#
# We require 2 arguments for this script:
# (1) The name of the .csv file to be scraped
# (2) The name of the column that contains email addresses
#
# Usage: python3 webscraper_script.py (1) (2)
num_arguments = len(sys.argv) - 1
if num_arguments != 2:
    print("Incorrect number of arguments.")
    print("Please check [insert wiki link] for instructions on how to use this script.")
    exit()

# Reading the given arguments 
csv_file_name = sys.argv[1]
email_col_name = sys.argv[2]

# Importing the .csv into a dataframe, and checking if arguments are valid
members_csv = pd.read_csv(csv_file_name)
if not email_col_name in members_csv:
    print("Given column name does not exist in dataframe.")
    exit()

# Filtering out deactivated accounts IFF .csv file is downloaded from Slack
if 'status' in members_csv:
    not_deactivated = members_csv['status'] != 'Deactivated'
    members_csv = members_csv[not_deactivated]

# Filtering out active members IFF .csv file is downloaded from Slack
if 'billing-active' in members_csv:
    inactive = members_csv['billing-active'] != 1
    members_csv = members_csv[inactive]

# Extracting emails and creating dataframe to hold results
member_activity = members_csv[[email_col_name]].copy()
member_activity['in_directory'] = 'nan' 

# Scraping @berkeley.edu emails from the cal directory, stalling between requests to avoid 403 forbidden 
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
does_not_exist = 'No matches to your search. Please try again.'
base_URL = "https://www.berkeley.edu/directory/results"
indices = member_activity.index

for i in range(len(member_activity)):
    member = member_activity.iloc[i]
    query = '?search-term=' + member[email_col_name].replace('@', '%40')
    full_query = base_URL + query
    page = requests.get(full_query, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    search_results = soup.find_all('section', {'class': 'search-results'})
    
    for result in search_results:
        if does_not_exist in result.text:
            member_activity.at[indices[i], 'in_directory'] = 0
        else:
            member_activity.at[indices[i], 'in_directory'] = 1  

    print(str(member[email_col_name]) + " " + str(does_not_exist in result.text))
    time.sleep(5)

# Filtering out slack members that exist in the cal directory and writing .csv to a new file  
graduated = member_activity['in_directory'] == 0
graduated_members = member_activity[graduated]
graduated_members.to_csv('graduated_members.csv')