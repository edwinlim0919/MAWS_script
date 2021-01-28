# IEEE Slack Member Webscraper
This repository contains Python scripts that automate Slack member management by
scraping email queries from the Cal Directory https://www.berkeley.edu/directory.
The resulting .csv file will contain emails of people who no longer attend Berkeley,
meaning these emails can be deleted from the Slack. Written and maintained by the
Technical Operations committee of IEEE@berkeley.

## System Requirements
I recommend using a virtual environment to run these scripts.
More information can be found at: 
https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/.

#### Python version: 
Python 3.9.1

#### Necessary Packages:
pandas, time, requests, sys, bs4

## csv_merger.py
This script is meant for merging emails from different .csv files together. It can be
used to get rid of duplicate emails and outputs a .csv file with all unique emails
from the .csv files provided as input. 

Usage: python3 webscraper_script.py filename_1 colname_1 filename_2 colname_2 ... 

filename_x: the xth .csv file to merge
colname_x:  name of the column that contains email addresses for the xth .csv file 

Output: Result will be put in all_emails.csv after script completes

## directory_scraper.py
This script is meant for the actual webscraping. It scrapes email queries from the Cal
Directory, keeping track of whether the email was present in the directory or not. In 
order to avoid getting a 403 forbidden error for requesting too quickly, the script 
waits 5 seconds between each query. So, leave it on in the background while you do 
something else. 

Usage: Usage: python3 webscraper_script.py filename colname

filename: the name of the .csv file containing the emails to scrape
colname:  the name of the column that contains email addresses for the .csv file

Output: Result will be put in graduated_members.csv after script completes