#!/usr/bin/env python3
import ast
import csv
import datetime
import os
import platform
import re
import sys
import time

import progressbar
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common import options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

'''
                                     DEFAULT DIRECTORY STRUCTURE
                                         (Do Not Change)
                                                ||
                                        [[[Parent Directory]]]
                                                |
                                                |
                                        ------------------
                                        |                |
                                        |                |
                                    [[Data]]          [[Scripts]](all scripts file here)
                                        |
                                    ---------------
                                    |             |
(Portable chrome + chromedriver)[Chrome]        [Records](Database)
'''

class BetaBot:
    '''
    By default this class has a method for:
        1. Opening a website URL in the script's portable chrome browser(Headless by default). 
            Method name ----- StartBot()
        2. Quitting the portable chrome browser.
            Method name ----- SotpBot()

    If required to add options like '--no-sandbox', '--disable-extensions', etc or, disable the options then, 
    search for this comment 'The following block of codes will add desired options' by copying it, pressing (CTRL + f), pasting it and modify the options as needed.

    If required to add actions like clicking multiple times on buttons, typing and pressing enter and so on then,
    Just add extra method to this class and call it whenever needed.
    '''
    def __init__(self, url) -> None:
        self.link = url

    #This method opens the portable chrome browser and opens the provided link 'url'
    def StartBot(self):
        print("\nBOT IS BEING ACTIVATED...")

        #getting full path of parent folder into 'ais' variable
        os.chdir(os.path.pardir)
        ais = os.getcwd()
        os.chdir("Scripts")

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
        '''The lines of codes till here tells seleium where to look for the chromedriver'''

        #changing the default location selenium looks for google chrome application to our portable one inside 'Data\Chrome\GoogleChromePortable' directory and not ones installed on the computer for matching version of google chrome with chromedriver
        options = ChromiumOptions() 
        options.binary_location = os.path.join(ais, "Data\Chrome\GoogleChromePortable\GoogleChromePortable.exe")
        '''The above block of codes tells selenium to look for the given portable chrome browser and not the ones installed in the machine if there is any [Version of chrome and chromedriver matches]'''

        #The following block of codes will add desired options. Add or remove options as desired.
        options.headless = True#Running chrome in the background
        options.add_experimental_option("excludeSwitches", ["enable-logging"])#Disabling log outputs
        options.add_argument("--window-size=1920,1080")#Setting window size
        options.add_argument("--start-maximized")#Setting option to automatically maximize windows on startup
        # options.add_argument(f'user-agent={user_agent}')
        # options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--allow-running-insecure-content')
        # options.add_argument("--disable-extensions")
        # options.add_argument("--proxy-server='direct://'")
        # options.add_argument("--proxy-bypass-list=*")
        # options.add_argument('--disable-gpu')

        options.add_argument('--disable-infobars')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--no-sandbox')


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

        #The following block of codes will add desired options
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

        # enable browser logging
        dlog = DesiredCapabilities.CHROME
        dlog['goog:loggingPrefs'] = { 'browser':'ALL' } 

        #The follwing codes will run the portable chrome software and open 'https://immi.homeaffairs.gov.au/visas/working-in-australia/skill-occupation-list' automatically
        self.driver = webdriver.Chrome(options=options, desired_capabilities=dlog)
        self.driver.get(self.link)        

    #First 
    def Store_SOL(self):
        #The two lines of codes below are used to find how many times our script has to perform an action similar to performing a left mouse click on button inside the website
        indexing_list = re.findall(r"Showing\s(\d\d)\sout\sof\s(\d\d\d)\sitems\sthat\smatch\syour\scriteria", self.driver.page_source)[0] #driver.page_source will give the source code of the currently opened webpage
        no_of_cliks_to_perform = int(indexing_list[1])//int(indexing_list[0])
        
        #Below 2 lines of codes are for initiating a loading status percentage bar
        widgets = ['RETRIEVING DATA: ', progressbar.Bar('=', '[', ']', '-'), progressbar.Percentage()]
        bar = progressbar.ProgressBar(max_value=no_of_cliks_to_perform+1,widgets=widgets,redirect_stdout=True).start() 


        #For finding titles which will be stored as list in 'headings'
        #The titles of the informations which are: [Occupation, ANZSCO code, Visa, List, Assessing authority] are inside the 'thead' element.
        table_head = self.driver.find_element(by=By.ID, value='table-search').find_element(by=By.ID, value='table-to-label-0').find_element(by=By.TAG_NAME, value="table").find_element(by=By.TAG_NAME, value="thead")
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
                table_body = self.driver.find_element(by=By.ID, value='table-search').find_element(by=By.ID, value='table-to-label-0').find_element(by=By.TAG_NAME, value="table").find_element(by=By.TAG_NAME, value="tbody") #This is a selenium object
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

                # if i == 0: #if first page
                #     #Now, we wait for a maximum of 20 seconds until the button 'Next' appears on the webpage.
                #     #Not doing this will result in inconsistent data being gather.
                #     el = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.PARTIAL_LINK_TEXT, "Next")) #This will provide a reference to the button we need to click
                #     #clicking the button now
                #     ActionChains(self.driver).click(el).perform()
                #     bar.update(i+1)

                # elif i !=0 and i != no_of_cliks_to_perform: #if second page to the last page
                #     el = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.PARTIAL_LINK_TEXT, "Next")) #This will provide a reference to the button we need to click
                #     ActionChains(self.driver).click(el).perform()

                #     '''--VERY IMPORTANT--'''
                #     #Now we make the script wait again until the chrome browser's console gives desired message as the last and the most recent log message
                #     #which is "hide blockui spinner...". When this log message is thrown to the console by the website, the websites fully loads the next page
                #     #Not doing this will result in inconsistent data being gather.
                #     while True: # looping until condition is fulfilled; new wait operation
                #         logg = self.driver.get_log('browser') #getting chrome browser's console log into a list of dictonaries
                #         if len(logg) == 0: #if browser gives no log in the console then we continue the loop
                #             continue
                #         else: #when there is log
                #             fgh = logg[-1] #retrieving the most recent log
                #             message = fgh['message'] #The above most recent log is a dictonary. Information we need is inside the key 'message' of this dict. So, storing the corresponding value of the key into a ariable
                #             if re.search(r'\"hide blockui spinner\.\.\.\"', message): #checking if the most recent log is the one we want & is so then breaking the loop
                #                 break
                #     bar.update(i+1)


                if i == 0: #if first page
                    try:
                        #Now, we wait for a maximum of 20 seconds until the button 'Next' appears on the webpage.
                        #Not doing this will result in inconsistent data being gather.
                        el = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.PARTIAL_LINK_TEXT, "Next")) #This will provide a reference to the button we need to click
                        #clicking the button now
                        ActionChains(self.driver).click(el).perform()
                    except:
                        #If the 'try' block fails the we quit the chrome browser and exit the program with message
                        bar.finish()
                        self.driver.quit()
                        sys.exit('\nWebsite took too long to load. Please run the script again!\n')
                    else:
                        bar.update(i+1)

                elif i !=0 and i != no_of_cliks_to_perform: #if second page to the last page
                    try:
                        el = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.PARTIAL_LINK_TEXT, "Next")) #This will provide a reference to the button we need to click
                        ActionChains(self.driver).click(el).perform()
                    except:
                        #If the 'try' block fails the we quit the chrome browser and exit the program with message
                        bar.finish()
                        self.driver.quit()
                        sys.exit('\nWebsite took too long to load. Please run the script again!\n')
                    else:
                        '''--VERY IMPORTANT--'''
                        #Now we make the script wait again until the chrome browser's console gives desired message as the last and the most recent log message
                        #which is "hide blockui spinner...". When this log message is thrown to the console by the website, the websites fully loads the next page
                        #Not doing this will result in inconsistent data being gather.
                        while True: # looping until condition is fulfilled; new wait operation
                            logg = self.driver.get_log('browser') #getting chrome browser's console log into a list of dictonaries
                            if len(logg) == 0: #if browser gives no log in the console then we continue the loop
                                continue
                            else: #when there is log
                                fgh = logg[-1] #retrieving the most recent log
                                message = fgh['message'] #The above most recent log is a dictonary. Information we need is inside the key 'message' of this dict. So, storing the corresponding value of the key into a ariable
                                if re.search(r'\"hide blockui spinner\.\.\.\"', message): #checking if the most recent log is the one we want & is so then breaking the loop
                                    break
                        bar.update(i+1)

            #Once the loop finishes, we tell our status bar that our objective is complete and satus bar shows 100%
            bar.finish()

    def SOL_Report_Generator(self):
        '''This function generates a txt report using the previously stored datas in "Data\Records" directory'''
        os.chdir('../Data/Records')
        files = os.listdir()

        print()
        print("\n-- Database of Skilled Occupation List Australia available from {} to {} ---".format((files[0].split("."))[0], (files[-1].split("."))[0]))
        print("-- NOTE: If the script doesn't find the exact match of the dates entered then, it will automatically provide report using the dates nearest to the ones entered in the database ---")
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

        os.chdir(os.path.pardir) #report file will be stored in this directory

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
                    #KK is in this format: [{}, {}]
                    by.write(pp + "\n\n")
                    for num,ui in enumerate(kk):
                        #ui is in this format: {}
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

    def IT_Jobs_Only(self):
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
    
        '''Now we either print information on screen or store information on a file as per user input'''
        #Now we ask input if user wants to print the information in the terminal or to create a report file inside 'WEBSCRAPPING\Data' directory
        o = True
        while o == True:
            print()
            from_user = input("Do you want to print the information here in the terminal or, create a report file?\nNOTE: Entering (y) will print the information here in the terminal and entering (n) will create a report file\n [y/n]: ").lower()
            if from_user == 'y':
                for i in range(1, len(processed_list)):
                    print()
                    headers = processed_list[0]
                    initial = processed_list[i]

                    print(f'({files_csv[-1].split(".")[0]}) IT occupations present in Skilled Occupation List of Australia:\n\n')
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
                    for m in range(1, len(processed_list)):
                        headers = processed_list[0]
                        initial = processed_list[m]

                        f.write(f'({files_csv[-1].split(".")[0]}) IT occupations present in Skilled Occupation List of Australia:\n\n')
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
                
                
                os.chdir(os.path.join(os.path.pardir, "Data"))
                print("\nDone!!\nGo to '{}' and open '(SOL-Aus)IT_JOBS_REPORT.txt'.\n\n".format(os.getcwd()))
                os.chdir(os.path.join(os.path.pardir, "Scripts"))
                
                o = False
            else:
                print("--Please provide a valid input: 'y' or 'n'--")

    def StopBot(self):
        self.driver.quit()

if __name__ == '__main__':
    # first = BetaBot(url="https://immi.homeaffairs.gov.au/visas/working-in-australia/skill-occupation-list")
    # first.StartBot()
    # first.Store_SOL()
    # first.StopBot()

    usr_in = sys.argv[1].lower()
    first = BetaBot(url="https://immi.homeaffairs.gov.au/visas/working-in-australia/skill-occupation-list")

    print("\n-- SOME PART OF THIS SCRIPT REQUIRES INTERNET CONNECTION.")

    if usr_in == 'help':
        print("\n-- GO TO THE DIRECTORY OF 'aussol.py' AND RUN COMMANDS ACCORDING TO YOUR NEED")
        print("\n1.(REQUIRES INTERNET) TO STORE TODAY'S SKILLED OCCUPATION LIST OF AUSTRALIA IN THE DATABASE:\n\t[RUN: aussol.py<space>store]")
        print("\n\n2.GENERATE A REPORT OF ALL OCCUPATION IN SKKILLED OCCUPATION LIST OF AUSTRALIA:\n\tA. (REQUIRES INTERNET) TO MAKE A REPORT OF LATEST INFORMATION:\n\t\t[RUN FIRST: aussol.py<space>store]\n\t\t[RUN SECOND: aussol<space>reportALL]\n\n\tB. (INTERNET NOT REQUIRED) TO MAKE REPORT FROM THE SCRIPT'S DATABASE:\n\t\t[RUN: aussol<space>reportALL]")
        print("\n\n2.GENERATE A REPORT OF ONLY IT OCCUPATION IN SKKILLED OCCUPATION LIST OF AUSTRALIA:\n\tA. (REQUIRES INTERNET) TO MAKE A REPORT OF LATEST INFORMATION:\n\t\t[RUN FIRST: aussol.py<space>store]\n\t\t[RUN SECOND: aussol<space>reportIT]\n\n\tB. (INTERNET NOT REQUIRED) TO MAKE REPORT FROM THE MOST RECENT RECORD IN SCRIPT'S DATABASE:\n\t\t[RUN: aussol<space>reportIT]\n")

    elif usr_in == 'store':
        try:
            #Below two codes for checking internet connection
            main_link = "https://www.google.com"
            webpage_object = requests.get(main_link, timeout=3)

        except (requests.ConnectionError, requests.Timeout) as exception:
            sys.exit("\nCannot store data when offline. Please run this argument again when internet is available.")
        else:
            #Checking whether SOL of the current date is already stored in database
            #If it already exists then it will skip the below block of code and only if it doesn't exist then it will run the function to store SOL of the current date
            os.chdir(os.path.join(os.path.pardir, r"Data\Records"))
            if not os.path.isfile(f"{datetime.datetime.today().strftime('%Y-%m-%d')}.csv"): 
                try:
                    #print("\n---------------------------------------------------------------------------------------------------------------------------")
                    print("-- THIS PROCESS USUALLY TAKES AROUND 2 TO 3 MINUTES. PLEASE DO NOT EXIT WHILE THE SCRIPT GATHERS NECESSARY LATEST DATAS\n") 
                    os.chdir('../../Scripts')  
                    first.StartBot()
                    first.Store_SOL()
                    
                    print(f"\n{datetime.datetime.today().strftime('%Y-%m-%d')} copy of Skilled Occupation List Australia is now stored and, can be used to generate report.")
                    print("---------------------------------------------------------------------------------------------------------------------------\n")
                except:
                    if os.path.isfile(f"{datetime.datetime.today().strftime('%Y-%m-%d')}.csv"): 
                        current_date = datetime.datetime.today().strftime('%Y-%m-%d')
                        os.remove(f'{current_date}.csv')    
                        sys.exit('\nSorry. Some error occured during the retrieval process.')
                    else:
                        sys.exit('\nSorry. Some error occured during the retrieval process.')
                
            else:
                print("\n++Today's Skilled Occupation List already stored++\n")
                os.chdir('../../Scripts')  

    elif usr_in == 'reportall':
        first.SOL_Report_Generator()

    elif usr_in == 'reportit':
        first.IT_Jobs_Only()
        
    else:
        sys.exit("\nPlease enter one of following arguments after aussol.py with an space in between.\n  Enter command like this: aussol<space><argument>\n\t\targuments: 1. 'store' for storing today's Skilled Occupation List\n\t\t           2. 'reportALL' for generating report of all occupations between two dates\n\t\t           3. 'reportIT' for  generating report of only IT occupations")
