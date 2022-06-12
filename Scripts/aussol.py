#!/usr/bin/env python3
import requests
import time
from bs4 import BeautifulSoup
import re
import csv
import sys
import os
import datetime
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common import options
import platform
import ast
import progressbar

def store_current_SOL():
    '''This function uses chrome bot(selenium) to open "https://immi.homeaffairs.gov.au/visas/working-in-australia/skill-occupation-list" which then scrapes data from the currently opened webpage and click the "Next" button and again scrape data and on goes the loop until there is no "Next" button.
    The reason why selenium is used instead of directly modifying the webpage URL for web scrapping is because in the above website, there are no clear links to land on desired webpages by modifying URLs. Instead, a selenium bot is designed to gather data and interact with the website. '''
    
    #changing the default location which selenium looks for finding google chrome application to our portable one inside 'Data\Chrome\GoogleChromePortable' directory
    options = ChromiumOptions() 
    options.binary_location = os.path.join(ais, "Data\Chrome\GoogleChromePortable\GoogleChromePortable.exe")

    #setting the path to out chromedriver in 'PATH' environment variable so we dont have to mention it in --driver = webdriver.Chrome()--
    os_system_name = str(platform.system()).lower()
    if re.search(r"win", os_system_name):#When running on windows
        initial = os.environ['PATH']
        path = os.path.join(ais, "Data\Chrome\chromedriver_win32")
        if path not in str(os.environ['PATH']):
            os.environ['PATH'] += path
            final = os.environ['PATH']
            if final[-(len(path)+1)] == initial[-1]:
                ff = initial + ";" + path
                os.environ['PATH'] = ff
    elif re.search(r"mac", os_system_name):#when running on mac
        initial = os.environ['PATH']
        path = os.path.join(ais, "Data\Chrome\chromedriver_mac64")
        if path not in str(os.environ['PATH']):
            os.environ['PATH'] += path
            final = os.environ['PATH']
            if final[-(len(path)+1)] == initial[-1]:
                ff = initial + ";" + path
                os.environ['PATH'] = ff
    elif re.search(r"linux", os_system_name):#When running on linux
        initial = os.environ['PATH']
        path = os.path.join(ais, "Data\Chrome\chromedriver_linux64")
        if path not in str(os.environ['PATH']):
            os.environ['PATH'] += path
            final = os.environ['PATH']
            if final[-(len(path)+1)] == initial[-1]:
                ff = initial + ";" + path
                os.environ['PATH'] = ff

    #The following block od codes will add desired options
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_experimental_option("excludeSwitches", ["enable-logging"])#Running chrome in the background
    options.add_argument("--window-size=1920,1080")#Setting window size
    options.add_argument("--start-maximized")#Setting option to automatically maximize windows on startup
    # options.add_argument(f'user-agent={user_agent}')
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--allow-running-insecure-content')
    # options.add_argument("--disable-extensions")
    # options.add_argument("--proxy-server='direct://'")
    # options.add_argument("--proxy-bypass-list=*")
    # options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--no-sandbox')

    print("BOT IS BEING ACTIVATED...")
    #The follwing codes will run the portable chrome software and open 'https://immi.homeaffairs.gov.au/visas/working-in-australia/skill-occupation-list' automatically
    driver = webdriver.Chrome(options=options)
    driver.get("https://immi.homeaffairs.gov.au/visas/working-in-australia/skill-occupation-list")

   #The two lines of codes below are used to find how many times our script has to perform an action similar to performing a left mouse click on button inside the website
    indexing_list = re.findall(r"Showing\s(\d\d)\sout\sof\s(\d\d\d)\sitems\sthat\smatch\syour\scriteria", driver.page_source)[0] #driver.page_source will give the source code of the currently opened webpage
    no_of_cliks_to_perform = int(indexing_list[1])//int(indexing_list[0])

    #Below 2 lines of codes are for initiating a loading status percentage bar
    widgets = ['RETRIEVING DATA: ', progressbar.Bar('=', '[', ']', '-'), progressbar.Percentage()]
    bar = progressbar.ProgressBar(max_value=no_of_cliks_to_perform+1,widgets=widgets).start() 


    #For finding titles which will be stored as list in 'headings'
    #The titles of the informations which are: [Occupation, ANZSCO code, Visa, List, Assessing authority] are inside the 'thead' element.
    table_head = driver.find_element(by=By.ID, value='table-search').find_element(by=By.ID, value='table-to-label-0').find_element(by=By.TAG_NAME, value="table").find_element(by=By.TAG_NAME, value="thead")
    table_head = table_head.get_attribute('innerHTML')
    headings = re.findall(r"\<th\>([\w\s]+)\<\/th\>", str(table_head))

    #Appending an extra element to the the 'heading list' which will act as title for the sixth column of our final data
    headings.append("For more information: ")

    #So, now a file with title as the current date and extension '.csv' is created inside 'WEBSCRAPPING\Data\Records' folder and data in 'processed_list' is stored there
    current_date = datetime.datetime.today().strftime('%Y-%m-%d')
    with open(f'../Data/Records/{current_date}.csv','w') as f:
        writer = csv.writer(f, delimiter="#")
        writer.writerow(headings)
    
        #We have to click the 'Next' button by 'no_of_cliks_to_perform'
        for i in range(0, no_of_cliks_to_perform+1):
            #The rest of all the information we need is inside 'tbody' element
            table_body = driver.find_element(by=By.ID, value='table-search').find_element(by=By.ID, value='table-to-label-0').find_element(by=By.TAG_NAME, value="table").find_element(by=By.TAG_NAME, value="tbody") #This is a selenium object
            table_body = table_body.get_attribute('innerHTML') #Converting selenium object into html format
            web = BeautifulSoup(table_body, 'html.parser') #Finally, converting into BeautifulSoup4 object
            each_row = web.find_all("tr") #Keeping all instances of 'tr' element insde 'tbody' element in a list

            #Below list variable will store information of all occupations present in the currently opened webpage in the selenuim chrome browser in a list(nested).
            twenty = []

            #looping through each element of list 'each_row'
            for each in each_row: 
                
                #Since there are some useless 'tr' elements present in the webpage, we will filter the ones important to us
                if not re.search(r"\<tr\sclass\=\"accordion-content\"\shidden\=\"\"\>\s+.+\s+<\/tr\>", str(each)):
                    #Here each usefull element of the list 'each_row' has 5 'td elements'. So, we again make it into a list.
                    tr = each.find_all("td")
                    
                    #Below 'Val" variable is currently an empty list but will be populated will information related to a single occupation in SOL
                    val = []

                    #Again we loop through the elements of 'tr' list and filter out just the data we need and everytime append any useful info to 'val' list
                    for td in tr:
                        if str(td) == str(tr[0]) or str(td) == str(tr[3]):
                            if not re.findall(r"\<td\>([\w\s\S]+)\<\/", str(td)):
                                val.append("")
                            else:
                                val.append(re.findall(r"\<td\>([\w\s\S]+)\<\/", str(td))[0])
                        elif str(td) == str(tr[1]):
                            if not re.search(r"\<td\>.+\"\>(\w+)\<\/", str(td)):
                                val.append("")
                            else:
                                val.append(re.search(r"\<td\>.+\"\>(\w+)\<\/", str(td))[1])
                        elif str(td) == str(tr[2]):
                            if not re.findall(r'\<li\>([\s\w\d()"–-]+)\<', str(td)):
                                val.append("")
                            else:
                                val.append(re.findall(r'\<li\>([\s\w\d()"-]+)\<', str(td)))
                        elif str(td) == str(tr[4]):
                            if not re.search(r'sub-heading"\>([\w\s]+)\<\/span', str(td)):
                                val.append("")
                            else:
                                val.append(re.search(r'sub-heading"\>([\w\s]+)\<\/span', str(td))[1])
                    
                    #list variable 'val' has the needed 5 elements but we want to add links to each occupations where user can go to to learn more about that particular job
                    #Appending an element to sixth column of our data
                    val.append(f"https://www.yourcareer.gov.au/careers/{val[1]}")
                    
                    #Appending a row to the list variable 'twenty'
                    twenty.append(val)

            #Now the 'twenty' list variable has the processed data of all occupations present in currently opened chrome browser
            #We write it the above mentioned csv file
            writer.writerows(twenty)

            #Initializing 'twenty' variable as an empty list for storing data of the another webpage which will be opened after running the below codes.
            twenty = []

            if i != no_of_cliks_to_perform:
                try:
                    '''--VERY IMPORTANT--'''
                    #Now, we wait for a maximum of 20 seconds until the button 'Next' appears on the webpage.
                    #Not doing this will result in inconsistent data being gather.
                    el = WebDriverWait(driver, timeout=20).until(lambda d: d.find_element(By.PARTIAL_LINK_TEXT, "Next")) #This will provide a reference to the button we need to click

                    #clicking the button now
                    ActionChains(driver).click(el).perform()
                except:
                    #If the 'try' block fails the we quit the chrome browser and exit the program with message
                    bar.finish()
                    driver.quit()
                    sys.exit('\nWebsite took too long to load. Please run the script again!\n')
                
                #Below code will update the position of the status bar and update the percentage shown.
                bar.update(i+1)
            else:
                break
        #Once the loop finishes, we tell our status bar that our objective is complete and satus bar shows 100%
        bar.finish()
    
    #Quitting the chrome browser if everything works and the scrip doesn't have to go to the 'except' block in the above loop
    driver.quit()
        


def SOL_report_generator():
    '''This function generates a txt report using the previously stored datas in "Data\Records" directory'''
    os.chdir('../Data/Records')
    files = os.listdir()

    print()
    print("\n--- Database of Skilled Occupation List Australia available from {} to {} ---".format((files[0].split("."))[0], (files[-1].split("."))[0]))
    print("--- NOTE: If the script doesn't find the exact match of the dates entered then, it will automatically provide report using the dates nearest to the ones entered in the database ---")
    print("\nEnter dates between ({}) and ({}) in the format (YYYY-MM-DD) for manuallly giving the dates or,\nJust press ('Enter') key twice for using the oldest and the most recent date in the databse.".format(str((files[0].split("."))[0]), str((files[-1].split("."))[0])))
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

        #splitting "YYYY-MM-DD" into ['YYYY', 'MM', 'DD'] list
        a1 = user_in_start.split("-")
        #checking if first digit of the second element of the list 'a1' starts with '0'. If so, then removing that '0' and keeping everything else as it is
        if a1[1][0] == '0':
            to_insert = a1[1][1]
            a1.pop(1)
            a1.insert(1, to_insert)
        #checking if first digit of the third element of the list 'a1' starts with '0'. If so, then removing that '0' and keeping everything else as it is
        if a1[2][0] == '0':
            to_insert = a1[2][1]
            a1.pop(2)
            a1.insert(2, to_insert)

        #same as above
        a2 = user_in_end.split("-")
        if a2[1][0] == '0':
            to_insert = a2[1][1]
            a2.pop(1)
            a2.insert(1, to_insert)
        if a2[2][0] == '0':
            to_insert = a2[2][1]
            a2.pop(2)
            a2.insert(2, to_insert)

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
                    by.write(f'\t{str(nn+1)}. [{str(jk[keys_[0]])}]\n')
                    by.write(f'\t\t{str(keys_[1])}: {str(jk[keys_[1]])}\n')

                    #The element of the list 'jk[keys_[2]]' is also a list which python converted into string. So, using evaluation method of 'ast' library we can safely convert it into a list
                    x = ast.literal_eval(jk[keys_[2]])
                    x = [n.strip() for n in x]
                    for gg in x: #jk[keys_[2]] is a list
                        if gg == x[0]:
                            by.write(f'\t\t{str(keys_[2])}: {str(gg)}\n')
                        else:
                            by.write(f'\t\t      {gg}\n')

                    by.write(f'\t\t{str(keys_[3])}: {str(jk[keys_[3]])}\n')
                    by.write(f'\t\t{str(keys_[4])}: {str(jk[keys_[4]])}\n')
                    by.write(f'\t\t{str(keys_[5])}: {str(jk[keys_[5]])}\n')
                    by.write(r"----------------------------------------------------------------------------------------------------------------------" + "\n\n")
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
    '''This function returns information related to IT jobs listed in SOL from the database'''

    os.chdir('../Data/Records')
    files_csv = os.listdir()

    with open('{}'.format(files_csv[-1])) as ff:
        reader = csv.reader(ff, delimiter="#")
        initial_list_variable = []
        for i in reader:
            initial_list_variable.append(i)
    initial_li = initial_list_variable

    #Below list will have just the data related to IT occupations
    processed_list = []

    #The following code will add the titles of the data to the begining of the list "processed_list"
    processed_list.append(initial_li[0])

    #Now we loop through the elements of "initial_li" list and filter the information we need using regex
    for i in initial_li:
        keywords = [r"ICT.*", r"[Cc]omputer.*", r"[Cc]ommunication.*", r"Software.*", r"Web.*", r"Programmer.*", r"Network.*", r"Database.*", r"261112", r"135111", r"262113", r"263211", r"263212", r"263213", r"263299", r"313111", r"313112", r"313113", r"313199", r"313211", r"313212", r"313213", r"313214", r"261313", r"261312", r"261211", r"263111"]
        for bb in keywords:
            if re.search(bb, str(i)) and i not in processed_list:
                processed_list.append(i)
    os.chdir("../../Scripts")
    return processed_list
def IT_jobs_only_output(input_list):
    '''This function is continuation of IT_jobs_only() function which either prints information on screen or stores information on a file as per user input'''
    #Now we ask input if user wants to print the information in the terminal or to create a report file inside 'WEBSCRAPPING\Data' directory
    o = True
    while o == True:
        print()
        from_user = input("Do you want to print the information here in the terminal or, create a report file?\nNOTE: Entering (y) will print the information here in the terminal and entering (n) will create a report file\n [y/n]: ").lower()
        if from_user == 'y':
            for i in range(1, len(input_list)):
                print()
                headers = input_list[0]
                initial = input_list[i]

                print('\n')
                print(f'{str(i)}. [{initial[0]}]\n')
                print(f'\t{headers[1]}: {initial[1]}\n')

                #The element of the list 'initial' is also a list which python converted into string. So, using evaluation method of 'ast' library we can safely convert it into a list
                x = ast.literal_eval(initial[2]) 
                x = [n.strip() for n in x]
                #looping through and writing each element of the list 'x' into a new line
                for b in x:
                    if b == x[0]:
                        print(f'\t{headers[2]}:   {b}\n')
                    else:
                        print(f'\t\t{b}\n')

                print(f'\t{headers[3]}: {initial[3]}\n')
                print(f'\t{headers[4]}: {initial[4]}\n')
                print(f'\t{headers[5]}: {initial[5]}\n')
                print(r"-----------------------------------------------------------------------------------------------------------------")

            o = False
        elif from_user == 'n':
            with open(os.path.join(os.path.pardir, f"Data\(SOL-Aus)IT_JOBS_REPORT.txt"),"w") as f:
                for m in range(1, len(input_list)):
                    headers = input_list[0]
                    initial = input_list[m]

                    f.write('\n')
                    f.write(f'{str(m)}. [{initial[0]}]\n')
                    f.write(f'\t{headers[1]}: {initial[1]}\n')

                    #The element of the list 'initial' is also a list which python converted into string. So, using evaluation method of 'ast' library we can safely convert it into a list
                    x = ast.literal_eval(initial[2]) 
                    x = [n.strip() for n in x]
                    #looping through and writing each element of the list 'x' into a new line
                    for b in x:
                        if b == x[0]:
                            f.write(f'\t{headers[2]}:   {b}\n')
                        else:
                            f.write(f'\t\t{b}\n')

                    f.write(f'\t{headers[3]}: {initial[3]}\n')
                    f.write(f'\t{headers[4]}: {initial[4]}\n')
                    f.write(f'\t{headers[5]}: {initial[5]}\n')
                    f.write(r"------------------------------------------------------------------------------------------------------------")
                    f.write("\n")
            
            print()
            os.chdir(os.path.join(os.path.pardir, "Data"))
            print("\nDone!!\nGo to '{}' and open '(SOL-Aus)IT_JOBS_REPORT.txt'.\n".format(os.getcwd()))
            print()
            os.chdir(os.path.join(os.path.pardir, "Scripts"))
            
            o = False
        else:
            print("--Please provide a valid input: 'y' or 'n'--")



def user_interaction():
    ''''This function is used to enable user interaction with the script in terminal'''
    print()
    print("NOTE:\n('y' for yes)\n('n' for no)\n('e' for exit)")
    print("\n")
    a = True
    while a == True:

        b = True
        while b ==True:
            user_1 = input("Do you want to generate Skilled Occupation List report? [y/n/e]: ").lower()
            if user_1 == "y":
                SOL_report_generator()

                e = True
                while e==True:
                    user_final2 = input("\nDo you want continue again? [y/n]: ").lower()
                    print()
                    if user_final2 == "y":
                        a = True
                        e = False
                    elif user_final2 == "n":
                        a = False
                        b = False
                        e = False
                    else:
                        print("--Please provide a valid input - 'y' or 'n' or 'e'--\n")
        
            elif user_1 == "n":
                c = True
                while c == True:
                    user_2 = input("\nDo you want to get a latest report of only IT occupations currently present in Skilled Occupation List of Australia? [y/n/e]: ").lower()
                    if user_2 == "y":
                        IT_jobs_only_output(IT_jobs_only())
                        user_final3 = input("\nDo you want continue again? [y/n]: ").lower()
                        print()
                        f = True
                        while f==True:
                            if user_final3 == "y":
                                f = False
                            elif user_final3 == "n":
                                a = False
                                b = False
                                c = False
                                f = False
                            else:
                                print("--Please provide a valid input - 'y' or 'n' or 'e'--\n")

                    elif user_2 == "n":
                        g = True
                        while g==True:
                            user_final = input("\nDo you want continue again? [y/n]: ").lower()
                            print()
                            if user_final == "y":
                                a = True
                                g = False
                            elif user_final == "n":
                                a = False
                                b = False
                                c = False
                                g = False
                            else:
                                print("--Please provide a valid input - 'y' or 'n' or 'e'--\n")
                        
                    elif user_2 == "e":
                        a = False
                        b = False
                        c = False
                    else:
                        print("--Please provide a valid input - 'y' or 'n' or 'e'--\n")
                    
            elif user_1 == "e":
                a = False
                b = False
            else:
                print("--Please provide a valid input - 'y' or 'n' or 'e'--\n")

if __name__ == "__main__":
    try:
        print("\nSOME PART OF THIS SCRIPT REQUIRES INTERNET CONNECTION.")

        #Below two codes for checking internet connection
        main_link = "https://www.google.com"
        webpage_object = requests.get(main_link, timeout=3)
        
        print("-Internet Connection Available-\n")
        print()
        print(r"[This script retrives information about occupation from Skilled Occupation List(SOL) of Australia  and stores a copy of current SOL for making reports]")
        print("[In addition, you can request to make a report of changes that took place between two dates in the Skilled Occupation List or]")
        print("[You can request to retrive the latest information about only IT occupations present in the Skilled Occupation List]")
        print()

        #getting full path of WebScrapping folder into 'ais' variable
 
        os.chdir(os.path.pardir)
        ais = os.getcwd()
        os.chdir("Scripts")

        #changing the default location selenium looks for google chrome application to our portable one inside 'Data\Chrome\GoogleChromePortable' directory and not ones installed on the computer for matching version of google chrome with chromedriver
        options = ChromiumOptions() 
        options.binary_location = os.path.join(ais, "Data\Chrome\GoogleChromePortable\GoogleChromePortable.exe")

        #setting the path to out chromedriver in 'PATH' environment variable so we dont have to mention it in --driver = webdriver.Chrome()--
        os_system_name = str(platform.system()).lower()
        if re.search(r"win", os_system_name):#When running on windows
            initial = os.environ['PATH']
            path = os.path.join(ais, "Data\Chrome\chromedriver_win32")
            if path not in str(os.environ['PATH']):
                os.environ['PATH'] += path
                final = os.environ['PATH']
                if final[-(len(path)+1)] == initial[-1]:
                    ff = initial + ";" + path
                    os.environ['PATH'] = ff
        elif re.search(r"mac", os_system_name):#when running on mac
            initial = os.environ['PATH']
            path = os.path.join(ais, "Data\Chrome\chromedriver_mac64")
            if path not in str(os.environ['PATH']):
                os.environ['PATH'] += path
                final = os.environ['PATH']
                if final[-(len(path)+1)] == initial[-1]:
                    ff = initial + ";" + path
                    os.environ['PATH'] = ff
        elif re.search(r"linux", os_system_name):#When running on linux
            initial = os.environ['PATH']
            path = os.path.join(ais, "Data\Chrome\chromedriver_linux64")
            if path not in str(os.environ['PATH']):
                os.environ['PATH'] += path
                final = os.environ['PATH']
                if final[-(len(path)+1)] == initial[-1]:
                    ff = initial + ";" + path
                    os.environ['PATH'] = ff

    #following except block will be initialted whenever there is no internet connection
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("-No internet connection-\n")
        print()
        print("[You can request to make a report of changes that took place between two dates in the Skilled Occupation List or]")
        print("[You can request to retrive information about IT occupations from the most recent record of the Skilled Occupation List stored in script's databse]")
        print()
        user_interaction()

    else:
        #Checking whether SOL of the current date is already stored in database
        #If it already exists then it will skip the below block of code and only if it doesn't exist then it will run the function to store SOL of the current date
        os.chdir(os.path.join(os.path.pardir, r"Data\Records"))
        if not os.path.isfile(f"{datetime.datetime.today().strftime('%Y-%m-%d')}.csv"): 
            print("\n------------------------------------------------------------------------------------------------------------------------\n")
            print("+++THIS PROCESS USUALLY TAKES AROUND 2 TO 3 MINUTES. PLEASE WAIT WHILE THE SCRIPT GATHERS NECESSARY LATEST DATAS+++\n") 
            os.chdir('../../Scripts')  
            store_current_SOL()
            print(f"{datetime.datetime.today().strftime('%Y-%m-%d')} copy of Skilled Occupation List Australia is now stored and, can be used to generate report.")
            print("\n------------------------------------------------------------------------------------------------------------------------\n")
        else:
            print("\n++Today's Skilled Occupation List already stored++\n")
            os.chdir('../../Scripts')  

        user_interaction()