#!/usr/bin/env python3
import os

def delete_all_report_files():
    '''This function or this script will delte all the report files which Webscrapping.py generates inside Data folder'''
    
    #name of the first report file
    all_jobs = r'(SOL-Aus)ALL_JOBS_REPORT.txt'

    #name of the seconf report file
    it_jobs = r'(SOL-Aus)IT_JOBS_REPORT.txt'

    #change directory to the parent folder and then to Data folder
    os.chdir(os.path.pardir)
    os.chdir('Data')

    #check if the report files are already created
    if os.path.isfile(all_jobs) and os.path.isfile(it_jobs):
        #Now delete the files
        os.remove(all_jobs)
        os.remove(it_jobs)
        print('\nThe report files are deleted.\n')
    else:
        print('\nThere are no report files created yet.\nRun WebScrapping.py to create it.\n')

delete_all_report_files()
