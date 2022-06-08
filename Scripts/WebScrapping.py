#!/usr/bin/env python3
from cgitb import text
import enum
import requests
from bs4 import BeautifulSoup
import re
import csv
import os
import datetime


def current_SOL():
    '''This function returns a list SOL data'''
    #'tbody' in turn has many child elements 'tr'
    all_jobs_html = Aus_SOL_list.contents #Data here is stored in HTML format which contains all jobs in SOL

    #Below list will have just the data we need, not in HTML format but, in a list like: ['Occupation', 'ANZSCO code', 'List', 'Visa Subclasses(Streams or type)', 'Assessing Authority']
    processed_list = [] 

    #Since data in 'all_jobs_html' is still in HTML format, for loop and regex is used to filter out just the information needed
    for i in all_jobs_html:
        #The following two lines of code will store the titles of data like: ['Occupation', 'ANZSCO code', 'List', 'Visa Subclasses(Streams or type)', 'Assessing Authority']
        if i == all_jobs_html[0]:
            processed_list.append(re.findall(r"\<th\sstyle\=\"height\:\s\d\dpx\;\"\>\<span\sstyle\=\"font\-weight\:\s\d\d\d\;\"\>([\w\s,()\/]+)\<\/span\>", str(i)))
        #The following two lines of code will add information about the jobs to 'processed_list' list
        else:
            to_append = re.findall(r"\"\>([\w\s,()\/*]+)\<\/td\>", str(i))
            if "removed" not in to_append:
                processed_list.append(to_append)
            #processed_list.append(re.findall(r"\<td\sstyle\=\"height\:\s\d\dpx\;\"\>([\w\s,()\/*]+)\<\/td\>", str(i.find_all("td"))))

    #processed_list is no longer empty and has a list of every jobs in SOL
    return processed_list
def store_current_SOL(input_list):
    '''This is continuation of the function store_current_SOL() and will store the given input into a new file'''
    initial = input_list

    #So, now a file with title as the current date and extension '.csv' is created inside 'WEBSCRAPPING\Data\Records' folder and data in 'processed_list' is stored there
    current_date = datetime.datetime.today().strftime('%Y-%m-%d')
    with open(os.path.join(os.path.pardir, f"Data\Records\{current_date}.csv"), "w") as f:
        writer = csv.writer(f, delimiter="#")
        for row in initial:
            writer.writerow(row)
    print()
    print(f"{current_date} copy of Skilled Occupation List Australia is now stored and, can be used to generate report.")
    print()


def SOL_report_generator():
    '''This function generates a txt report using the previously stored datas in "Data\Records" directory'''
    os.chdir(os.path.join(os.path.pardir, r"Data\Records"))

    files = os.listdir()
    print()
    print("\n--- Database of Skilled Occupation List Australia available from {} to {} ---".format((files[0].split("."))[0], (files[-1].split("."))[0]))
    print("--- NOTE: If the script doesn't find the exact match of the dates entered then, it will automatically provide report using the dates nearest to the ones entered in the database ---")
    print("\nEnter dates between ({}) and ({}) in the format (YYYY-MM-DD) for manuallly giving the dates or,\nJust press ('Enter') key twice for using the oldest and the most recent date in the databse.".format((files[0].split("."))[0], (files[-1].split("."))[0]))
    print()
    #Checking if input from user is a valid date in given format
    con = False
    while con == False:
        con1 = False
        while con1 == False:
            user_in_start = input("Enter start date: ")
            if re.match(r"^\d{4}[.;:\/\\~,|-]\d{2}[.;:\/\\~,|-]\d{2}", user_in_start):
                a,b,c = user_in_start.split("-")
                try:
                    if datetime.datetime(int(a),int(b),int(c)):
                        con1 = True
                except ValueError as v:
                    print(v)
            elif user_in_start == "":
                guf = files[0].split(".")
                user_in_start = guf[0]
                con1 = True
            else:
                print("Please enter the date in a valid format: (YYYY-MM-DD)")
            
        con2 = False
        while con2 == False:
            user_in_end = input("Enter end date: ")
            if re.match(r"^\d{4}[.;:\/\\~,|-]\d{2}[.;:\/\\~,|-]\d{2}", user_in_end):
                a,b,c = user_in_end.split("-")
                try:
                    if datetime.datetime(int(a),int(b),int(c)):
                        con2 = True
                except ValueError as v:
                    print(v)
            elif user_in_end == "":
                guf = files[-1].split(".")
                user_in_end = guf[0]
                con2 = True
            else:
                print("Please enter the date in a valid format: (YYYY-MM-DD)")

        a1 = user_in_start.split("-")
        a2 = user_in_end.split("-")
        start_date = datetime.datetime(int(a1[0]), int(a1[1]), int(a1[2]))
        end_date = datetime.datetime(int(a2[0]), int(a2[1]), int(a2[2]))
        if start_date < end_date:
            con = True
        else:
            print("End date should be older than start date!")


    #Find the nearest date to the given input if it is valid
    test_date_list = []
    for file in files:
        e = file.split(".")
        v = e[0]
        x,y,z = v.split("-")
        
        try:
            if datetime.datetime(int(x),int(y),int(z)):
                test_date_list.append(datetime.datetime(int(x),int(y),int(z)))
        except ValueError:
            continue

    #For start date and end date
    date_list = [start_date, end_date]
    nearest_dates = []
    for qq in date_list:
        cloz_dict = {abs(qq.timestamp() - date.timestamp()) : date for date in test_date_list}
        res = cloz_dict[min(cloz_dict.keys())]
        nearest_dates.append(str(res.date()))

    #nearest_dates list has a list of nearest start and end date of user input

    #opening the files with names provided by "nearest_dates list"
    start_date_dict = []
    with open(nearest_dates[0] + ".csv") as h:
            reader = csv.DictReader(h, delimiter="#")
            for u in reader:
                start_date_dict.append(u)

    end_date_dict = []
    with open(nearest_dates[1] + ".csv") as f:
        reader = csv.DictReader(f, delimiter="#")
        for j in reader:
            end_date_dict.append(j)

    #prv will store every element of csv file corresponding to the nearest user given start date that is not in csv file corresponding to the nearest user given end date 
    prv = []
    for g in start_date_dict:
        if g not in end_date_dict:
            prv.append(g)
    #prv will store every element of csv file corresponding to the nearest user given end date that is not in csv file corresponding to the nearest user given start date 
    curr = []
    for y in end_date_dict:
        if y not in start_date_dict:
            curr.append(y)

    account = {}

    if len(curr) == 0 and len(prv) != 0:
        nam = nearest_dates[0] + " to " + nearest_dates[1] + "; " + str(len(prv)) + " jobs removed from Skilled Occupation List Australia: "
        account[nam] = prv
        account[f"All {str(len(end_date_dict))} currently available jobs in Skilled Occupation List Australia: "] = end_date_dict
    elif len(curr) != 0 and len(prv) == 0:
        nam = nearest_dates[0] + " to " + nearest_dates[1] + "; " + str(len(curr)) + " jobs added to Skilled Occupation List Australia: "
        account[nam] = curr
        account[f"All {str(len(end_date_dict))} currently available jobs in Skilled Occupation List Australia: "] = end_date_dict
    elif len(curr) == 0 and len(prv) == 0:
        nam = nearest_dates[0] + " to " + nearest_dates[1] + "; " + " No changes in Skilled Occupation List Australia; " + str(len(end_date_dict)) + " occupations present currently: "
        account[nam] = end_date_dict
    else:
        nam = nearest_dates[0] + " to " + nearest_dates[1] + "; " + str(len(prv)) + " jobs removed and, " + str(len(curr)) + " new jobs added in Skilled Occupation List Australia: "
        combined = [prv, curr]
        account[nam] = combined
        account[f"All {str(len(end_date_dict))} currently available jobs in Skilled Occupation List Australia: "] = end_date_dict
    #account is no longer empty and contains all the info we need

    os.chdir(os.path.pardir)

    with open("(SOL-Aus)ALL_JOBS_REPORT.txt","w") as by:
        for pp,kk in account.items():
            if len(kk) != 2:
                keys_ = list(kk[0].keys())
                by.write(pp + "\n\n")
                for nn,jk in enumerate(kk):
                    by.write("\t" + str(nn+1) + ". [" + str(jk[keys_[0]]) + "]" + "\n")
                    by.write("\t\t" + str(keys_[1]) + ": " + str(jk[keys_[1]]) + "\n")
                    by.write("\t\t" + str(keys_[2]) + ": " + str(jk[keys_[2]]) + "\n")
                    by.write("\t\t" + str(keys_[3]) + ": " + str(jk[keys_[3]]) + "\n")
                    by.write("\t\t" + str(keys_[4]) + ": " + str(jk[keys_[4]]) + "\n")
                    by.write("\n")
                by.write(r"----------------------------------------------------------------------------------------------------------------------" + "\n\n\n")
            elif len(kk) == 2:
                #[{}, {}]
                by.write(pp + "\n\n")
                for num,ui in enumerate(kk):
                    #{}
                    keys_ = list(ui[0].keys())
                    if num == 0:
                        by.write("\t****Removed jobs are listed below:")
                        by.write("\n")
                    if num == 1:
                        by.write("\t****Added jobs are listed below:")
                        by.write("\n")
                    for nn,jk in enumerate(ui):
                        by.write("\t\t" + str(nn+1) + ". [" + str(jk[keys_[0]]) + "]" + "\n")
                        by.write("\t\t\t" + str(keys_[1]) + ": " + str(jk[keys_[1]]) + "\n")
                        by.write("\t\t\t" + str(keys_[2]) + ": " + str(jk[keys_[2]]) + "\n")
                        by.write("\t\t\t" + str(keys_[3]) + ": " + str(jk[keys_[3]]) + "\n")
                        by.write("\t\t\t" + str(keys_[4]) + ": " + str(jk[keys_[4]]) + "\n")
                        by.write("\n")
                    by.write(r"----------------------------------------------------------------------------------------------------------------------" + "\n\n\n")
    print("\nDone!!\nGo to '{}' and open '(SOL-Aus)ALL_JOBS_REPORT.txt'.\n".format(os.getcwd()))
    os.chdir(os.path.join(os.path.pardir, r"Scripts"))



def IT_jobs_only():
    '''This function returns information related to IT jobs listed in SOL'''
    print("\n____Please wait a few moments____")
    #'tbody' in turn has many child elements 'tr'
    all_jobs_html = Aus_SOL_list.find_all("tr") #Data here is stored in HTML format which contains all jobs in SOL

    #Below list will have just the data related to IT jobs in HTML format
    processed_list = []

    #The following block of code will add the titles of the data to the begining of the list "processed_list"
    r = 0
    for q in all_jobs_html:
        if r == 1:
            break
        processed_list.append(q)
        r+=1

    #Now we loop through the elements of "processed_list" list and filter the information we need using regex
    for i in all_jobs_html:
        keywords = [r"ICT.*", r"[Cc]omputer.*", r"[Cc]ommunication.*", r"Software.*", r"Web.*", r"Programmer.*", r"Network.*", r"Database.*", r"261112", r"135111", r"262113", r"263211", r"263212", r"263213", r"263299", r"313111", r"313112", r"313113", r"313199", r"313211", r"313212", r"313213", r"313214", r"261313", r"261312", r"261211", r"263111"]
        for bb in keywords:
            if re.search(bb, str(i)) and i not in processed_list:
                processed_list.append(i)

    #Below list will have just the data we need, not in HTML format but, in a list like: ['Occupation', 'ANZSCO code', 'List', 'Visa Subclasses(Streams or type)', 'Assessing Authority']
    processed_list_final = []

    #Since data in 'processed_list' is still in HTML format, for loop and regex is used to filter out just the information needed
    for k in processed_list:
        if k == processed_list[0]:
            processed_list_final.append(re.findall(r"\<th\sstyle\=\"height\:\s\d\dpx\;\"\>\<span\sstyle\=\"font\-weight\:\s\d\d\d\;\"\>([\w\s,()\/]+)\<\/span\>", str(k)))
        else:
            processed_list_final.append(re.findall(r"\<td\sstyle\=\"height\:\s\d\dpx\;\"\>([\w\s,()\/]+)\<\/td\>", str(k.find_all("td"))))

    #'processed_list_final' is no longer empty and has a list of information related to IT jobs given in SOL
    #from 'processed_list_final' taking only 'ANZSCO code' to generate a website link
    only_anzsco = []
    for n in processed_list_final:
        if n == processed_list_final[0]:
            only_anzsco.append('For more information: ')
        else:
            only_anzsco.append(n[1])
    #"only_anzsco" is no longer empty
    #Below variable will store websites of all jobs in SOL
    weblinks = []
    for code in only_anzsco:
        if code == only_anzsco[0]:
            weblinks.append(code)
        else:
            weblinks.append("https://www.yourcareer.gov.au/careers/" + code)

    #Below variable will store information from both "processed_list_final" and weblinks
    to_return = []
    for w, element in enumerate(processed_list_final):
        initial = element
        initial.append(weblinks[w])
        to_return.append(initial)
    return to_return
def IT_jobs_only_output(input_list):
    '''This function is continuation of IT_jobs_only() function which either prints information on screen or stores information on a file as per user input'''
    processed_list_final = input_list
    #Now we ask input if user wants to print the information in the terminal or to create a report file inside 'WEBSCRAPPING\Data' directory
    o = True
    while o == True:
        print()
        from_user = input("Do you want to print the information here in the terminal or, create a report file?\nNOTE: Entering (y) will print the information here in the terminal and entering (n) will create a report file\n [y/n]: ").lower()
        if from_user == 'y':
            for i in range(1, len(processed_list_final)):
                print()
                headers = processed_list_final[0]
                initial = processed_list_final[i]
                print(str(i) + ". ["+initial[0]+"]")
                print()
                print("\t" + headers[1] + r": " + initial[1])
                print("\t" + headers[2] + r": " + initial[2])
                print("\t" + headers[3] + r": " + initial[3])
                print("\t" + headers[4] + r": " + initial[4])
                print()
                print("\t" + headers[5] + r": " + initial[5])
                print(r"------------------------------------------------------------------------------------------------------------")

            o = False
        elif from_user == 'n':
            with open(os.path.join(os.path.pardir, f"Data\(SOL-Aus)IT_JOBS_REPORT.txt"),"w") as f:
                for m in range(1, len(processed_list_final)):
                    headers = processed_list_final[0]
                    initial = processed_list_final[m]
                    f.write("\n")
                    f.write(str(m) + ". ["+initial[0]+"]")
                    f.write("\n")
                    f.write("\t" + headers[1] + r": " + initial[1] + "\n")
                    f.write("\t" + headers[2] + r": " + initial[2] + "\n")
                    f.write("\t" + headers[3] + r": " + initial[3] + "\n")
                    f.write("\t" + headers[4] + initial[4] + "\n")
                    f.write("\n")
                    f.write("\t" + headers[5] + initial[5] + "\n")
                    f.write(r"------------------------------------------------------------------------------------------------------------")
                    f.write("\n")
            os.chdir(os.path.join(os.path.pardir, "Data"))
            print()
            print("Done!!")
            os.chdir(os.path.pardir)
            location_var = os.getcwd()
            os.chdir("Scripts")
            print("--Go to '{}' and open '(SOL-Aus)IT_JOBS_REPORT.txt'.".format(os.path.join(location_var, "Data")))
            print()
            os.chdir(os.path.join(os.path.pardir, "Scripts"))
            
            o = False
        else:
            print("--Please provide a valid input: 'y' or 'n'--")


if __name__ == "__main__":
    print("\nSome parts of this script requires internet connection.")
    try:
        #Information is taken from the following webpage
        main_link = "https://www.australianskilledmigration.com.au/skilled-occupations-list/"
        webpage_object = requests.get(main_link, timeout=4)
        webpage = BeautifulSoup(webpage_object.text, "html.parser")
        #The data we require is inside class: "table-main-outer" which has a child element 'tbody'
        Aus_SOL_list = webpage.find(class_="table-main-outer").tbody
        print("-Internet Connection Available-\n")
        print()
        print(r"This script retrives information about occupation from Skilled Occupation List(SOL) of Australia  and stores a copy of current SOL whenever requested.")
        print("In addition, you can request to make a report of changes that took place between two dates in the Skilled Occupation List or,")
        print("You can request to retrive current information about IT occupations present currently in the Skilled Occupation List")
        print()
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("-No internet connection-\n") 
        user_1 = input("Do you want to generate Skilled Occupation List report? [y/n]: ").lower()
        a = True
        while a == True:
            if user_1 == "y":
                SOL_report_generator()
                a = False
            elif user_1 == "n":
                a = False
            else:
                print("--Please provide a valid input - 'y' or 'n'--")
                a = False
    else:
        a = True
        while a == True:
            print()
            print("NOTE:\n('y' for yes)\n('n' for no)\n('e' for exit)")
            print("\n")
            user = input("Do you want to store current Skilled Occupation List of Australia? [y/n/e]: ").lower()
            if user == "y":
                store_current_SOL(current_SOL())
                user_final1 = input("Do you want continue again? [y/n/e]: ").lower()
                if user_final1 == "y":
                    a = True
                elif user_final1 == "n":
                    a = False
                elif user_final1 == "e":
                    a = False
                else:
                    print("+++Please provide a valid input - 'y' or 'n' or 'e'+++")
                    print()
            elif user == "n":
                user_1 = input("Do you want to generate Skilled Occupation List report? [y/n/e]: ").lower()
                if user_1 == "y":
                    store_current_SOL(current_SOL())
                    SOL_report_generator()
                    user_final2 = input("Do you want continue again? [y/n/e]: ").lower()
                    if user_final2 == "y":
                        a = True
                    elif user_final2 == "n":
                        a = False
                    elif user_final2 == "e":
                        a = False
                    else:
                        print("+++Please provide a valid input - 'y' or 'n' or 'e'+++")
                        print()
                elif user_1 == "n":
                    user_2 = input("Do you want to get an uptodate report of only IT jobs in Skilled Occupation List? [y/n/e]: ").lower()
                    if user_2 == "y":
                        IT_jobs_only_output(IT_jobs_only())
                        user_final3 = input("Do you want continue again? [y/n/e]: ").lower()
                        if user_final3 == "y":
                            a = True
                        elif user_final3 == "n":
                            a = False
                        elif user_final3 == "e":
                            a = False
                        else:
                            print("+++Please provide a valid input - 'y' or 'n' or 'e'+++")
                            print()
                    elif user_2 == "n":
                        user_final = input("Do you want continue again? [y/n/e]: ").lower()
                        if user_final == "y":
                            a = True
                        elif user_final == "n":
                            a = False
                        elif user_final == "e":
                            a = False
                        else:
                            print("+++Please provide a valid input - 'y' or 'n' or 'e'+++")
                            print()
                    elif user_2 == "e":
                        a = False
                    else:
                        print("+++Please provide a valid input - 'y' or 'n' or 'e'+++")
                        print()
                elif user_1 == "e":
                    a = False
                else:
                    print("+++Please provide a valid input - 'y' or 'n' or 'e'+++")
                    print()
                
            elif user == "e":
                a = False
            else:
                print("+++Please provide a valid input - 'y' or 'n' or 'e'+++")
                print()