# **Australia's Skilled Occupation List report generator - v2.1**


* First of all, go to the 'Scripts' directory in the terminal.
* Secondly, run "del_reports.py" to remove any existing report files.
* Finally, run the command "aussol.py help" and follow the instructions.

> **NOTE:**
All scripts are inside **'Scripts'** folder and the database directory of the script is **'Data/Records'**.\
If you want to see the project's default directory tree then, open 'aussol.py' in a code editor or IDE and scroll just below the import section.

<pre>
<b>FORMAT:
$ ausso.py{space}{attributtes}</b>
                        |
			---------> store (Refer to action no. 1)
			|
			---------> reportALL (Refer to action no. 2)
			|
			---------> reportIT (Refer to action no. 3)
</pre>
## You can request the script to perform the following (three actions):

#### 1. ***(REQUIRES INTERNET)*** To store the latest copy of the Skilled Occupation List (SOL) of Australia in the script's database(Data/Records):
	
> ***$ aussol.py store***

&nbsp;&nbsp;&nbsp;&nbsp;
After running above command the script automatically stores latest Skilled Occupation List of current date into its database only if there is an internet connection and current date's Skilled Occupation List entry is not stored in the database yet.
#### 2. ***(INTERNET NOT REQUIRED)*** To generate Skilled Occupation List report (all occupations) from the script's database:

> ***$ aussol.py reportALL***

&nbsp;&nbsp;&nbsp;&nbsp;
Running the above command will generate an Skilled Occupation List report of all occupations between two desired dates from script's database.\

&nbsp;&nbsp;&nbsp;&nbsp;
If in case, the script's database does not have Skilled Occupation List of the entered dates then, it will automatically choose dates nearest to it in its database to generate a report file.
	
&nbsp;&nbsp;&nbsp;&nbsp;
Depending on the information stored in the entered date's Skilled Occupation List entry, the script will create a report file which could include any of the following details:\
<font size = "2">
* No changes with all the current occupation present in the latest Skilled Occupation List.
* Added occupations with its total number and all the current occupation present in the latest Skilled Occupation List.
* Removed occupations with its total number and all the current occupations present in the latest Skilled Occupation List.
* Both added as well as removed occupations with its total number and all the current occupations present in the latest Skilled Occupation List.
</font>

#### 3. ***(INTERNET NOT REQUIRED)*** To generate latest Skilled Occupation List report (IT related occupations only) from the script's database:

> ***$ aussol.py reportIT***
		
&nbsp;&nbsp;&nbsp;&nbsp;
Running the above command will generate IT occupations report from Skilled Occupation List of Australia and the script will ask whether user wants to recieve the report on the terminal or as a report file


### This script has two modes:
	
	1. When internet connectivity is available:
	
		All three above actions can be performed.
		

	2. When there is no internet connection:
	
		Only the second and the third action can be performed.	


### If you want only the latest information:
	
	First, perform action no. 1 then, either of 2nd, 3rd or both action s(one after another).
