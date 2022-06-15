#!/usr/bin/env python3
import ast
import csv
import datetime
import os
import platform
import re
import sys
import time

from tqdm import tqdm
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

from fpdf import FPDF, HTMLMixin
from fpdf.enums import XPos, YPos

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

class PDF(FPDF, HTMLMixin):
    current0 = []
    def header(self):
        dir_checker = str(os.getcwd())
        if dir_checker.endswith("Records"):
            os.chdir("../../Scripts")
        # Rendering logo:

        #self.image("aus.png", 65, -16, 80)
        self.image("../Data/Resources/PDF/kang.svg", 95, 3, 20)
        self.set_font("helvetica", "B", 27)
        self.cell(80)

        self.ln()

        self.set_font("helvetica", "B", 17)
        self.cell(60)
        self.cell(70, 10, "Skilled occupation list", border=1, align="C")

        # Performing a line break:
        self.ln()

        if len(PDF.current0) == 1:
            #datetime.datetime.today().strftime('%Y-%m-%d')
            current = PDF.current0[0].split("-")
            y, m, d = current[0], current[1], current[2]
            if current[1][0]=='0':
                m = int(current[1][-1])
            if current[2][0]=='0':
                d = current[2][-1]
            M = ["Janurary", "February", "March", "April", "May", "June", "July", "August", "September", "August", "November", "December"]

            self.set_font("helvetica", size=14)
            self.cell(60)
            self.cell(70, 10, f"{str(d)} {str(M[m-1])}, {str(y)}", align="C")
            self.ln(15)
        elif len(PDF.current0) == 2:
            combined_dates = []
            for i in PDF.current0:
                current = i.split("-")
                y, m, d = current[0], current[1], current[2]
                if current[1][0]=='0':
                    m = int(current[1][-1])
                if current[2][0]=='0':
                    d = current[2][-1]
                M = ["Janurary", "February", "March", "April", "May", "June", "July", "August", "September", "August", "November", "December"]
                _txt = f"{str(d)} {str(M[m-1])}, {str(y)}"
                combined_dates.append(_txt)

            self.set_font("helvetica", size=14)
            self.cell(60)
            self.cell(70, 10, f"{combined_dates[0]} to {combined_dates[1]}", align="C")
            self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        #printing page number
        self.cell(0, 8, f"page {self.page_no()}/{{nb}}", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.cell(0,2,r"https://github.com/AbhashChamlingRai/AUS_SOL_Report_Generator", align="C")

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

    #Setting the link which chrome will open
    def __init__(self, url) -> None:
        self.link = url
    
    #this method will create the tablular information in the report pdf file
    def pdf_table(self, pdf_obj, in_d):
        '''Takes pdf object created in advance as first parameter and a list of dictonaries as the second parameter and creates a table of informations using loops'''
        pdf = pdf_obj
        titles_ = list(in_d[0].keys())        
        for mm, r in enumerate(in_d):
            mmm =mm + 1
            if len(str(mmm))==1:
                with pdf.offset_rendering() as dummy:
                    pdf.set_font(size=20)
                    pdf.cell(6)
                    #pdf.multi_cell(w=5,txt="1.")
                    pdf.cell(txt=f"{mm+1}.")
                    pdf.set_font(size=15)
                    pdf.multi_cell(align="C", w=170,h=10, border=1, txt=r[titles_[0]])
                    pdf.ln(0)

                    y= ast.literal_eval(r[titles_[2]])
                    y = [n.strip() for n in y]

                    abs_v = ''
                    for yu in y:
                        if yu == y[-1]:
                            abs_v += f'\t- {yu}'
                        else:
                            abs_v += f'\t- {yu}\n'

                    pdf.set_font(size=10)
                    pdf.cell(14)
                    pdf.multi_cell(align="L", w=170, border=1, txt=f'''
{titles_[1].upper()}:
--> {r[titles_[1]]}
{titles_[2].upper()}:
{abs_v}
{titles_[3].upper()}:
--> {r[titles_[3]]}
{titles_[4].upper()}:
--> {r[titles_[4]]}
{titles_[5].upper()}:
--> {r[titles_[5]]}
''')
                    pdf.ln(0)

                if dummy.page_break_triggered:
                    pdf.add_page()


                pdf.set_font(size=20)
                pdf.cell(6)
                #pdf.multi_cell(w=5,txt="1.")
                pdf.cell(txt=f"{mm+1}.")
                pdf.set_font(size=15)
                pdf.multi_cell(align="C", w=170,h=10, border=1, txt=r[titles_[0]])
                pdf.ln(0)

                y= ast.literal_eval(r[titles_[2]])
                y = [n.strip() for n in y]

                abs_v = ''
                for yu in y:
                    if yu == y[-1]:
                        abs_v += f'\t- {yu}'
                    else:
                        abs_v += f'\t- {yu}\n'

                pdf.set_font(size=10)
                pdf.cell(14)
                pdf.multi_cell(align="L", w=170, border=1, txt=f'''
{titles_[1].upper()}:
--> {r[titles_[1]]}
{titles_[2].upper()}:
{abs_v}
{titles_[3].upper()}:
--> {r[titles_[3]]}
{titles_[4].upper()}:
--> {r[titles_[4]]}
{titles_[5].upper()}:
--> {r[titles_[5]]}
''')
                pdf.ln(0)


            if len(str(mmm))==2:     
                with pdf.offset_rendering() as dummy:
                    pdf.set_font(size=20)
                    pdf.cell(2)
                    #pdf.multi_cell(w=5,txt="1.")
                    pdf.cell(txt=f"{mm+1}.")
                    pdf.set_font(size=15)
                    pdf.multi_cell(align="C", w=170,h=10, border=1, txt=r[titles_[0]])
                    pdf.ln(0)

                    y= ast.literal_eval(r[titles_[2]])
                    y = [n.strip() for n in y]

                    abs_v = ''
                    for yu in y:
                        if yu == y[-1]:
                            abs_v += f'\t- {yu}'
                        else:
                            abs_v += f'\t- {yu}\n'

                    pdf.set_font(size=10)
                    pdf.cell(14)
                    pdf.multi_cell(align="L", w=170, border=1, txt=f'''
{titles_[1].upper()}:
--> {r[titles_[1]]}
{titles_[2].upper()}:
{abs_v}
{titles_[3].upper()}:
--> {r[titles_[3]]}
{titles_[4].upper()}:
--> {r[titles_[4]]}
{titles_[5].upper()}:
--> {r[titles_[5]]}
''')
                    pdf.ln(0)

                if dummy.page_break_triggered:
                    pdf.add_page()


                pdf.set_font(size=20)
                pdf.cell(2)
                #pdf.multi_cell(w=5,txt="1.")
                pdf.cell(txt=f"{mm+1}.")
                pdf.set_font(size=15)
                pdf.multi_cell(align="C", w=170,h=10, border=1, txt=r[titles_[0]])
                pdf.ln(0)

                y= ast.literal_eval(r[titles_[2]])
                y = [n.strip() for n in y]

                abs_v = ''
                for yu in y:
                    if yu == y[-1]:
                        abs_v += f'\t- {yu}'
                    else:
                        abs_v += f'\t- {yu}\n'

                pdf.set_font(size=10)
                pdf.cell(14)
                pdf.multi_cell(align="L", w=170, border=1, txt=f'''
{titles_[1].upper()}:
--> {r[titles_[1]]}
{titles_[2].upper()}:
{abs_v}
{titles_[3].upper()}:
--> {r[titles_[3]]}
{titles_[4].upper()}:
--> {r[titles_[4]]}
{titles_[5].upper()}:
--> {r[titles_[5]]}
''')
                pdf.ln(0)

            if len(str(mmm))==3:     
                with pdf.offset_rendering() as dummy:
                    pdf.set_font(size=20)
                    pdf.cell(-2)
                    #pdf.multi_cell(w=5,txt="1.")
                    pdf.cell(txt=f"{mm+1}.")
                    pdf.set_font(size=15)
                    pdf.multi_cell(align="C", w=170,h=10, border=1, txt=r[titles_[0]])
                    pdf.ln(0)

                    y= ast.literal_eval(r[titles_[2]])
                    y = [n.strip() for n in y]

                    abs_v = ''
                    for yu in y:
                        if yu == y[-1]:
                            abs_v += f'\t- {yu}'
                        else:
                            abs_v += f'\t- {yu}\n'

                    pdf.set_font(size=10)
                    pdf.cell(14)
                    pdf.multi_cell(align="L", w=170, border=1, txt=f'''
{titles_[1].upper()}:
--> {r[titles_[1]]}
{titles_[2].upper()}:
{abs_v}
{titles_[3].upper()}:
--> {r[titles_[3]]}
{titles_[4].upper()}:
--> {r[titles_[4]]}
{titles_[5].upper()}:
--> {r[titles_[5]]}

''')
                    pdf.ln(0)

                if dummy.page_break_triggered:
                    pdf.add_page()


                pdf.set_font(size=20)
                pdf.cell(-2)
                #pdf.multi_cell(w=5,txt="1.")
                pdf.cell(txt=f"{mm+1}.")
                pdf.set_font(size=15)
                pdf.multi_cell(align="C", w=170,h=10, border=1, txt=r[titles_[0]])
                pdf.ln(0)

                y= ast.literal_eval(r[titles_[2]])
                y = [n.strip() for n in y]

                abs_v = ''
                for yu in y:
                    if yu == y[-1]:
                        abs_v += f'\t- {yu}'
                    else:
                        abs_v += f'\t- {yu}\n'

                pdf.set_font(size=10)
                pdf.cell(14)
                pdf.multi_cell(align="L", w=170, border=1, txt=f'''
{titles_[1].upper()}:
--> {r[titles_[1]]}
{titles_[2].upper()}:
{abs_v}
{titles_[3].upper()}:
--> {r[titles_[3]]}
{titles_[4].upper()}:
--> {r[titles_[4]]}
{titles_[5].upper()}:
--> {r[titles_[5]]}

''')
                pdf.ln(0)

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

    #This method uses selenium and beautifulsoup4 to scrape data and store in csv format
    def Store_SOL(self):
        '''Stores information from the website using selenium and beautifulsoup4'''
        #The two lines of codes below are used to find how many times our script has to perform an action similar to performing a left mouse click on button inside the website
        indexing_list = re.findall(r"Showing\s(\d\d)\sout\sof\s(\d\d\d)\sitems\sthat\smatch\syour\scriteria", self.driver.page_source)[0] #driver.page_source will give the source code of the currently opened webpage
        no_of_cliks_to_perform = int(indexing_list[1])//int(indexing_list[0])
        
        # #Below 2 lines of codes are for initiating a loading status percentage bar
        # widgets = ['RETRIEVING DATA: ', progressbar.Bar('=', '[', ']', '-'), progressbar.Percentage()]
        # bar = progressbar.ProgressBar(max_value=no_of_cliks_to_perform+1,widgets=widgets,redirect_stdout=True).start() 


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
            for i in tqdm(range(0, no_of_cliks_to_perform+1), desc="RETRIEVING DATA: ", ascii=False, ncols=75):
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

                if i == 0: #if first page
                    try:
                        #Now, we wait for a maximum of 20 seconds until the button 'Next' appears on the webpage.
                        #Not doing this will result in inconsistent data being gather.
                        el = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.PARTIAL_LINK_TEXT, "Next")) #This will provide a reference to the button we need to click
                        #clicking the button now
                        ActionChains(self.driver).click(el).perform()
                    except:
                        #If the 'try' block fails the we quit the chrome browser and exit the program with message
                        self.driver.quit()
                        sys.exit('\nWebsite took too long to load. Please run the script again!\n')

                elif i !=0 and i != no_of_cliks_to_perform: #if second page to the last page
                    try:
                        el = WebDriverWait(self.driver, timeout=20).until(lambda d: d.find_element(By.PARTIAL_LINK_TEXT, "Next")) #This will provide a reference to the button we need to click
                        ActionChains(self.driver).click(el).perform()
                    except:
                        #If the 'try' block fails the we quit the chrome browser and exit the program with message
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

    #This method generates pdf report of all occupation in skilled occupation list when called
    def All_jobs_Report_Generator(self):
        '''This function generates a pdf report using the previously stored data in "Data\Records" directory.
        It uses pdf_table() method of the parent class BetaBot to generate the data in table format'''

        os.chdir('../Data/Records')
        files = os.listdir()

        print("-- Database of Skilled Occupation List Australia available from {} to {}".format((files[0].split("."))[0], (files[-1].split("."))[0]))
        print("-- NOTE: If the script doesn't find the exact match of the dates entered then, it will automatically provide report using the dates nearest to the ones entered in the database")
        print("\nEnter dates between ({}) and ({}) in the format (YYYY-MM-DD) for manuallly giving the dates or,\nJust press ('Enter') key twice for using the oldest and the most recent date in the databse.\n".format(str((files[0].split("."))[0]), str((files[-1].split("."))[0])))

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

        print("\nPlease wait while the script generates report.")

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

        nearest_dates = []#this will have the nearest dates to the ones entered by user
        for qq in date_list:
            cloz_dict = {abs(qq.timestamp() - date.timestamp()) : date for date in test_date_list}
            res = cloz_dict[min(cloz_dict.keys())]
            nearest_dates.append(str(res.date()))

        #nearest_dates list has a list of nearest start and end date of user input

        #Below two will store only "ANZSCO code" of every element of a csv file in the database
        start = [] 
        end = []

        #Below two will store every element of a csv file in the database in dictionary format with not just the "ANZSCO code" but all the info
        start_dict = []
        end_dict = []

        #Opening csv file corresponding to the nearest user given start date
        with open(f'{nearest_dates[0]}.csv') as f:
            reader = csv.DictReader(f, delimiter="#")
            for i in reader:
                start.append(i["ANZSCO code"])
                start_dict.append(i)

        #Opening csv file corresponding to the nearest user given end date
        with open(f'{nearest_dates[-1]}.csv') as g:
            reader1 = csv.DictReader(g, delimiter="#")
            for j in reader1:
                end.append(j["ANZSCO code"])
                end_dict.append(j)


        intersection = list(set(end).intersection(start))
        intersection_dict = [] #(In dictionary)This will store every element that is common between csv file corresponding to the nearest user given start date and end date
        for mk in intersection:
            for kk in end_dict:
                if mk == kk["ANZSCO code"]:
                    intersection_dict.append(kk)

        only_in_start = list(set(start).difference(end))
        only_in_start_dict = [] #(In dictionary)this will will store every element of csv file corresponding to the nearest user given start date that is not in csv file corresponding to the nearest user given end date 
        for mk in only_in_start:
            for kk in start_dict:
                if str(mk) == kk["ANZSCO code"]:
                    only_in_start_dict.append(kk)


        only_in_end = list(set(end).difference(start))
        only_in_end_dict = [] #(In dictionary)this will store every element of csv file corresponding to the nearest user given end date that is not in csv file corresponding to the nearest user given start date 
        for mk in only_in_end:
            for kk in end_dict:
                if str(mk) == kk["ANZSCO code"]:
                    only_in_end_dict.append(kk)



        #Below two lines of code should be repeated evertime when a new pdf report file needs to be created so at to give the correct date in the pdf file
        #Giving the date of the csv file in the database from which we extracted the information to the class 'PDF'
        to_set = [nearest_dates[0], nearest_dates[1]] #date in which the most recent csv file was created
        PDF.current0 = to_set #giving it to the PDF class to set its class variable(current0) with the value of "to_set"

        #1st variable
        #Filtering visa list from every occupations in the latest entry of Skilled Occupation List in the database
        visa = []
        with open(f'{nearest_dates[1]}.csv') as f:
            reader = csv.DictReader(f, delimiter='#')
            for i in reader:
                kk = i["Visa"]
                x = ast.literal_eval(kk)
                x = [n.strip() for n in x]
                if len(x) == 1:
                    if x[0] not in visa:
                        visa.append(x[0])
                else:
                    for h in x:
                        if h not in visa:
                            visa.append(h)

        #2nd variable
        #Below list variable will store all the lists included in Skilled Occupation List of Australia but in short form like: ROL, STSOL, MLTSSL, etc
        sol_list_shortform = []
        with open(f'{nearest_dates[1]}.csv') as f:
            reader = csv.DictReader(f, delimiter='#')
            for i in reader:
                kk = i["List"]
                if kk not in sol_list_shortform:
                    if not re.search(r";|\s", str(kk)):
                        sol_list_shortform.append(kk.strip())
                    else:
                        if re.search(r";", str(kk)):
                            t = kk.split(";")
                            for num, j in enumerate(t):
                                if j.strip() not in sol_list_shortform:
                                    sol_list_shortform.append(j.strip())
                        if re.search(r" ", str(kk)):
                            t = kk.split(" ")
                            for num, j in enumerate(t):
                                if j.strip() not in sol_list_shortform:
                                    sol_list_shortform.append(j.strip())
        #Below list variable will store each and every element of 'sol_list_shortform' with its full-form appended to it
        sol_list_fullform = []
        for el in sol_list_shortform:
            if el.upper() == "ROL":
                sol_list_fullform.append(f"ROL - The Regional Occupation List")
            elif el.upper() == "STSOL":
                sol_list_fullform.append(f"STSOL - Short-term Skilled Occupation List")
            elif el.upper() == "MLTSSL":
                sol_list_fullform.append(f"MLTSSL - Medium and Long-term Strategic Skills List")
            elif el.upper() == "RSMS":
                sol_list_fullform.append(f"RSMS - Regional Sponsored Migration Scheme list")



        #3rd variable
        #storing names of assessing authorities from the latest entry in the database
        assessing_authorities = []
        with open(f'{nearest_dates[1]}.csv') as f:
            reader = csv.DictReader(f, delimiter='#')
            for i in reader:
                kk = i["Assessing authority"]
                if kk != '':
                    if kk not in assessing_authorities:
                        assessing_authorities.append(kk)


        os.chdir("../../Scripts")


        '''opening a pdf object in the script.... this won't make a file in the system... pdf.output() will'''
        pdf = PDF(format="a4")
        pdf.add_page() #adding a starting page


        '''1st section (Description & listing all visa types)'''
        #setting font size
        pdf.set_font(size=14)
        pdf.cell(12) #moving the ellement to be added 12 units to the right
        pdf.multi_cell(align="L", w=170, txt="The Skilled Occupation List is a list of current occupations eligible for different visa types. The following visas are available to individuals who are qualified to work or train in an eligible skilled occupation in Australia and can meet all other requirements:")
        pdf.ln(4) #Breaking line with 4 units

        pdf.set_font(size=13)
        for n,i in enumerate(visa): #printing visa list in the pdf file
            if n+1 < 10:
                pdf.cell(18)
                pdf.cell(txt=f"{n+1}.")
                pdf.cell(3)
                pdf.multi_cell(align="L", w=152, txt=f"{i}")
                pdf.ln(2)
            else:
                pdf.cell(18)
                pdf.cell(txt=f"{n+1}.")
                pdf.cell(1)
                pdf.multi_cell(align="L", w=152, txt=f"{i}")
                pdf.ln(2)
        pdf.ln(7)




        '''2nd section (giving all the list types in skilled occupation list)'''
        #for list types
        pdf.set_font(size=14)
        pdf.cell(12)
        pdf.multi_cell(align="L", w=170, txt="All the lists included in Skilled Occupation List of Australia:")
        pdf.ln(3)

        pdf.set_font(size=13) 
        for n,i in enumerate(sol_list_fullform): #printing all the sol list types in the pdf file
            pdf.cell(18)
            pdf.cell(txt=f"{n+1}.")
            pdf.cell(3)
            pdf.multi_cell(align="L", w=152, txt=f"{i}")
            pdf.ln(2)
        pdf.ln(7)




        '''3nd section (listing all assessing authorities in the Skilled Occupation List of Australia )'''
        pdf.set_font(size=14)
        pdf.cell(12)
        pdf.multi_cell(align="L", w=170, txt="All assessing authorities in the Skilled Occupation List of Australia:")
        pdf.ln(3)

        pdf.set_font(size=13)
        for n,i in enumerate(assessing_authorities):
            if n+1 < 10:
                pdf.cell(18)
                pdf.cell(txt=f"{n+1}.")
                pdf.cell(3)
                pdf.multi_cell(align="L", w=152, txt=f"{i}")
                pdf.ln(2)
            else:
                pdf.cell(18)
                pdf.cell(txt=f"{n+1}.")
                pdf.cell(1)
                pdf.multi_cell(align="L", w=152, txt=f"{i}")
                pdf.ln(2)

        if len(only_in_start_dict) != 0:
            pdf.add_page()
            pdf.set_font(size=14)
            pdf.cell(12)
            pdf.multi_cell(align="L", w=170, txt=f"{len(only_in_start_dict)} occupation removed from the Skilled Occupation List of Australia between {nearest_dates[0]} to {nearest_dates[-1]}:")
            pdf.ln(5)

            BetaBot.pdf_table(self, p=pdf, in_d=only_in_start_dict)

        
        if len(only_in_end_dict) != 0:
            pdf.add_page()
            pdf.set_font(size=14)
            pdf.cell(12)
            pdf.multi_cell(align="L", w=170, txt=f"{len(only_in_end_dict)} occupation added to the Skilled Occupation List of Australia between {nearest_dates[0]} to {nearest_dates[-1]}:")
            pdf.ln(5)

            BetaBot.pdf_table(self, p=pdf, in_d=only_in_end_dict)
        
        
        if len(only_in_start_dict) != 0 and len(only_in_end_dict) == 0:
            pdf.add_page()
            pdf.set_font(size=14)
            pdf.cell(12)
            pdf.multi_cell(align="L", w=170, txt=f"Initially, there were {len(start_dict)} occupations in Skilled Occupation List of Australia in {nearest_dates[0]}. {len(only_in_start_dict)} occupations got removed. Hence, {len(start_dict) - len(only_in_start_dict)} occupations remains currently in {nearest_dates[-1]}. They are listed below:")
            pdf.ln(5)

            BetaBot.pdf_table(self, p=pdf, in_d=intersection_dict)


        if len(only_in_start_dict) == 0 and len(only_in_end_dict) != 0:
            pdf.add_page()
            pdf.set_font(size=14)
            pdf.cell(12)
            pdf.multi_cell(align="L", w=170, txt=f"Initially, there were {len(start_dict)} occupations in Skilled Occupation List of Australia in {nearest_dates[0]}. {len(only_in_end_dict)} occupations were added. Hence, {len(start_dict) + len(intersection_dict)} occupations remains currently in {nearest_dates[-1]}. Added occupations are given above. The remaining {len(intersection_dict)} occupations are listed below:")
            pdf.ln(5)

            BetaBot.pdf_table(self, p=pdf, in_d=intersection_dict)
        
        if len(only_in_start_dict) != 0 and len(only_in_end_dict) != 0:
            pdf.add_page()
            pdf.set_font(size=14)
            pdf.cell(12)
            pdf.multi_cell(align="L", w=170, txt=f"Initially, there were {len(start_dict)} occupations in Skilled Occupation List of Australia in {nearest_dates[0]}. {len(only_in_start_dict)} occupations were removed and {len(only_in_end_dict)} added. Hence, {len(end_dict)} occupations remains currently in {nearest_dates[-1]}. Removed and added occupations are given above. The remaining {len(intersection_dict)} occupations are listed below:")
            pdf.ln(5)

            BetaBot.pdf_table(self, p=pdf, in_d=intersection_dict)

        if len(only_in_start_dict) == 0 and len(only_in_end_dict) == 0:
            pdf.add_page()
            pdf.set_font(size=14)
            pdf.cell(12)
            pdf.multi_cell(align="L", w=170, txt=f"There were {len(start_dict)} occupations in Skilled Occupation List of Australia in {nearest_dates[0]}. The number of occupations in {nearest_dates[-1]} remained constant. No occupations were added or removed between the given dates. List of all {len(end_dict)} occupations are given below: ")
            pdf.ln(5)

            BetaBot.pdf_table(self, pdf_obj=pdf, in_d=end_dict)


        pdf.output("../All_Occupation_Report_Aus.pdf")
        
        os.chdir("../")
        print(f"\nReport pdf file is stored in '{os.getcwd()}' directory as 'All_Occupation_Report_Aus.pdf'.")
        os.chdir("Scripts")

    #This method generates pdf report of only IT occupation in skilled occupation list when called
    def IT_jobs_Report_Generator(self):
        '''This function returns information related to IT jobs listed in SOL from the database.
        It uses pdf_table() method of the parent class BetaBot to generate the data in table format'''

        os.chdir('../Data/Records')
        files_csv = os.listdir()

        '''Now we either print information on screen or store information on a file as per user input'''
        #Now we ask input if user wants to print the information in the terminal or to create a report file inside 'WEBSCRAPPING\Data' directory
        o = True
        while o == True:
            print()
            from_user = input("Do you want to print the information here in the terminal or, create a report file?\nNOTE: Entering (y) will print the information here in the terminal and entering (n) will create a report file.\n[y/n]: ").lower()
            if from_user == 'y':
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

                print(f'\n{files_csv[-1].split(".")[0]}: {len(processed_list)} IT occupations present in Skilled Occupation List of Australia:\n')
                for i in range(1, len(processed_list)):
                    print()
                    headers = processed_list[0]
                    initial = processed_list[i]

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
                    print(r"-------------------------------------------------------------------------------------------------------------------")
                o = False
                sys.exit()
            
            elif from_user == 'n':
                with open('{}'.format(files_csv[-1])) as ff:
                    reader = csv.DictReader(ff, delimiter="#")
                    initial_list_variable = []
                    for i in reader:
                        initial_list_variable.append(i)
                initial_li = initial_list_variable

                #Below list will have just the data related to IT occupations
                processed_list = []

                #Now we loop through the elements of "initial_li" list and filter the information we need using regex
                for i in initial_li:
                    keywords = [r"ICT.*", r"[Cc]omputer.*", r"[Cc]ommunication.*", r"Software.*", r"Web.*", r"Programmer.*", r"Network.*", r"Database.*", r"261112", r"135111", r"262113", r"263211", r"263212", r"263213", r"263299", r"313111", r"313112", r"313113", r"313199", r"313211", r"313212", r"313213", r"313214", r"261313", r"261312", r"261211", r"263111"]
                    for bb in keywords:
                        if re.search(bb, str(i)) and i not in processed_list:
                            processed_list.append(i)
                o = False
                

                #Below two lines of code should be repeated evertime when a new pdf report file needs to be created so at to give the correct date in the pdf file
                #Giving the date of the csv file in the database from which we extracted the information to the class 'PDF'
                to_set = files_csv[-1].split(".")[0] #date in which the most recent csv file was created
                PDF.current0 = [to_set] #giving it to the PDF class to set its class variable(current0) with the value of "to_set"

                #1st variable
                #Filtering visa list from every occupations in the latest entry of Skilled Occupation List in the database
                visa = []
                with open(files_csv[-1]) as f:
                    reader = csv.DictReader(f, delimiter='#')
                    for i in reader:
                        kk = i["Visa"]
                        x = ast.literal_eval(kk)
                        x = [n.strip() for n in x]
                        if len(x) == 1:
                            if x[0] not in visa:
                                visa.append(x[0])
                        else:
                            for h in x:
                                if h not in visa:
                                    visa.append(h)

                #2nd variable
                #Below list variable will store all the lists included in Skilled Occupation List of Australia but in short form like: ROL, STSOL, MLTSSL, etc
                sol_list_shortform = []
                with open(files_csv[-1]) as f:
                    reader = csv.DictReader(f, delimiter='#')
                    for i in reader:
                        kk = i["List"]
                        if kk not in sol_list_shortform:
                            if not re.search(r";|\s", str(kk)):
                                sol_list_shortform.append(kk.strip())
                            else:
                                if re.search(r";", str(kk)):
                                    t = kk.split(";")
                                    for num, j in enumerate(t):
                                        if j.strip() not in sol_list_shortform:
                                            sol_list_shortform.append(j.strip())
                                if re.search(r" ", str(kk)):
                                    t = kk.split(" ")
                                    for num, j in enumerate(t):
                                        if j.strip() not in sol_list_shortform:
                                            sol_list_shortform.append(j.strip())
                #Below list variable will store each and every element of 'sol_list_shortform' with its full-form appended to it
                sol_list_fullform = []
                for el in sol_list_shortform:
                    if el.upper() == "ROL":
                        sol_list_fullform.append(f"ROL - The Regional Occupation List")
                    elif el.upper() == "STSOL":
                        sol_list_fullform.append(f"STSOL - Short-term Skilled Occupation List")
                    elif el.upper() == "MLTSSL":
                        sol_list_fullform.append(f"MLTSSL - Medium and Long-term Strategic Skills List")
                    elif el.upper() == "RSMS":
                        sol_list_fullform.append(f"RSMS - Regional Sponsored Migration Scheme list")



                #3rd variable
                #storing names of assessing authorities from the latest entry in the database
                assessing_authorities = []
                with open(files_csv[-1]) as f:
                    reader = csv.DictReader(f, delimiter='#')
                    for i in reader:
                        kk = i["Assessing authority"]
                        if kk != '':
                            if kk not in assessing_authorities:
                                assessing_authorities.append(kk)


                os.chdir("../../Scripts")


                '''opening a pdf object in the script.... this won't make a file in the system... pdf.output() will'''
                pdf = PDF(format="a4")
                pdf.add_page() #adding a starting page


                '''1st section (Description & listing all visa types)'''
                #setting font size
                pdf.set_font(size=14)
                pdf.cell(12) #moving the ellement to be added 12 units to the right
                pdf.multi_cell(align="L", w=170, txt="The Skilled Occupation List is a list of current occupations eligible for different visa types. The following visas are available to individuals who are qualified to work or train in an eligible skilled occupation in Australia and can meet all other requirements:")
                pdf.ln(4) #Breaking line with 4 units

                pdf.set_font(size=13)
                for n,i in enumerate(visa): #printing visa list in the pdf file
                    if n+1 < 10:
                        pdf.cell(18)
                        pdf.cell(txt=f"{n+1}.")
                        pdf.cell(3)
                        pdf.multi_cell(align="L", w=152, txt=f"{i}")
                        pdf.ln(2)
                    else:
                        pdf.cell(18)
                        pdf.cell(txt=f"{n+1}.")
                        pdf.cell(1)
                        pdf.multi_cell(align="L", w=152, txt=f"{i}")
                        pdf.ln(2)
                pdf.ln(7)




                '''2nd section (giving all the list types in skilled occupation list)'''
                #for list types
                pdf.set_font(size=14)
                pdf.cell(12)
                pdf.multi_cell(align="L", w=170, txt="All the lists included in Skilled Occupation List of Australia:")
                pdf.ln(3)

                pdf.set_font(size=13) 
                for n,i in enumerate(sol_list_fullform): #printing all the sol list types in the pdf file
                    pdf.cell(18)
                    pdf.cell(txt=f"{n+1}.")
                    pdf.cell(3)
                    pdf.multi_cell(align="L", w=152, txt=f"{i}")
                    pdf.ln(2)
                pdf.ln(7)




                '''3nd section (listing all assessing authorities in the Skilled Occupation List of Australia )'''
                pdf.set_font(size=14)
                pdf.cell(12)
                pdf.multi_cell(align="L", w=170, txt="All assessing authorities in the Skilled Occupation List of Australia:")
                pdf.ln(3)

                pdf.set_font(size=13)
                for n,i in enumerate(assessing_authorities):
                    if n+1 < 10:
                        pdf.cell(18)
                        pdf.cell(txt=f"{n+1}.")
                        pdf.cell(3)
                        pdf.multi_cell(align="L", w=152, txt=f"{i}")
                        pdf.ln(2)
                    else:
                        pdf.cell(18)
                        pdf.cell(txt=f"{n+1}.")
                        pdf.cell(1)
                        pdf.multi_cell(align="L", w=152, txt=f"{i}")
                        pdf.ln(2)

                
                pdf.add_page()
                BetaBot.pdf_table(self, pdf_obj=pdf, in_d=processed_list)
                pdf.output("../IT_Occupation_Report_Aus.pdf")
        
                os.chdir("../")
                print(f"\nReport pdf file is stored in '{os.getcwd()}' directory as 'IT_Occupation_Report_Aus.pdf'.")
                os.chdir("Scripts")
            else:
                print("--Please provide a valid input: 'y' or 'n'--")

    #This method quits the chrome browser
    def StopBot(self):
        self.driver.quit()

if __name__ == '__main__':

    try:
        usr_in = sys.argv[1].lower()
    except:
        print("\n-- AN ARGUMENT NEEDS TO BE GIVEN AFTER 'aussol.py' WITH A SPACE IN BETWEEN!")
        print("\n1.(REQUIRES INTERNET) TO STORE TODAY'S SKILLED OCCUPATION LIST OF AUSTRALIA IN THE DATABASE:\n\t[RUN: aussol.py<space>store]")
        print("\n\n2.GENERATE A REPORT OF ALL OCCUPATION IN SKKILLED OCCUPATION LIST OF AUSTRALIA:\n\tA. (REQUIRES INTERNET) TO MAKE A REPORT OF LATEST INFORMATION:\n\t\t[RUN FIRST: aussol.py<space>store]\n\t\t[RUN SECOND: aussol<space>reportALL]\n\n\tB. (INTERNET NOT REQUIRED) TO MAKE REPORT FROM THE SCRIPT'S DATABASE:\n\t\t[RUN: aussol<space>reportALL]")
        print("\n\n2.GENERATE A REPORT OF ONLY IT OCCUPATION IN SKKILLED OCCUPATION LIST OF AUSTRALIA:\n\tA. (REQUIRES INTERNET) TO MAKE A REPORT OF LATEST INFORMATION:\n\t\t[RUN FIRST: aussol.py<space>store]\n\t\t[RUN SECOND: aussol<space>reportIT]\n\n\tB. (INTERNET NOT REQUIRED) TO MAKE REPORT FROM THE MOST RECENT RECORD IN SCRIPT'S DATABASE:\n\t\t[RUN: aussol<space>reportIT]\n")
    else:
        first = BetaBot(url="https://immi.homeaffairs.gov.au/visas/working-in-australia/skill-occupation-list")
        if usr_in == 'help':
            print("\n-- SOME PART OF THIS SCRIPT REQUIRES INTERNET CONNECTION.")
            print("\n-- GO TO THE DIRECTORY OF 'aussol.py' AND RUN COMMANDS ACCORDING TO YOUR NEED")
            print("\n1.(REQUIRES INTERNET) TO STORE TODAY'S SKILLED OCCUPATION LIST OF AUSTRALIA IN THE DATABASE:\n\t[RUN: aussol.py<space>store]")
            print("\n\n2.GENERATE A REPORT OF ALL OCCUPATION IN SKKILLED OCCUPATION LIST OF AUSTRALIA:\n\tA. (REQUIRES INTERNET) TO MAKE A REPORT OF LATEST INFORMATION:\n\t\t[RUN FIRST: aussol.py<space>store]\n\t\t[RUN SECOND: aussol<space>reportALL]\n\n\tB. (INTERNET NOT REQUIRED) TO MAKE REPORT FROM THE SCRIPT'S DATABASE:\n\t\t[RUN: aussol<space>reportALL]")
            print("\n\n2.GENERATE A REPORT OF ONLY IT OCCUPATION IN SKKILLED OCCUPATION LIST OF AUSTRALIA:\n\tA. (REQUIRES INTERNET) TO MAKE A REPORT OF LATEST INFORMATION:\n\t\t[RUN FIRST: aussol.py<space>store]\n\t\t[RUN SECOND: aussol<space>reportIT]\n\n\tB. (INTERNET NOT REQUIRED) TO MAKE REPORT FROM THE MOST RECENT RECORD IN SCRIPT'S DATABASE:\n\t\t[RUN: aussol<space>reportIT]\n")

        elif usr_in == 'store':
            try:
                print("\n-- SOME PART OF THIS SCRIPT REQUIRES INTERNET CONNECTION.")
                #Below two codes for checking internet connection
                main_link = "https://www.google.com"
                webpage_object = requests.get(main_link, timeout=3)

            except (requests.ConnectionError, requests.Timeout) as exception:
                if os.path.isfile(f"../Data/Records/{datetime.datetime.today().strftime('%Y-%m-%d')}.csv"):
                    os.remove(f"../Data/Records/{datetime.datetime.today().strftime('%Y-%m-%d')}.csv")
                sys.exit("\nSorry. Cannot store data when offline. Please give this argument again when internet is available.")
            else:
                #Checking whether SOL of the current date is already stored in database
                #If it already exists then it will skip the below block of code and only if it doesn't exist then it will run the function to store SOL of the current date
                os.chdir(os.path.join(os.path.pardir, r"Data\Records"))
                if not os.path.isfile(f"{datetime.datetime.today().strftime('%Y-%m-%d')}.csv"): 
                    try:
                        print("-- THIS PROCESS USUALLY TAKES AROUND 2 TO 3 MINUTES. PLEASE DO NOT EXIT WHILE THE SCRIPT GATHERS NECESSARY LATEST DATAS\n") 
                        os.chdir('../../Scripts')  
                        first.StartBot()
                        first.Store_SOL()
                        
                        print(f"\n{datetime.datetime.today().strftime('%Y-%m-%d')} copy of Skilled Occupation List Australia is now stored and, can be used to generate report.")
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
            print("\n-- TO GET THE LATEST INFORMATION IN THE REPORT, RUN 'aussol store' FIRST AND THEN THIS ARGUMENT")
            first.All_jobs_Report_Generator()

        elif usr_in == 'reportit':
            print("\n-- TO GET THE LATEST INFORMATION IN THE REPORT, RUN 'aussol store' FIRST AND THEN THIS ARGUMENT")
            first.IT_jobs_Report_Generator()
            
        else:
            sys.exit("\nPlease enter one of following arguments after aussol.py with an space in between.\n  Enter command like this: aussol<space><argument>\n\t\tArguments: 1. 'store' for storing today's Skilled Occupation List\n\t\t           2. 'reportALL' for generating report of all occupations between two dates\n\t\t           3. 'reportIT' for  generating report of only IT occupations")
