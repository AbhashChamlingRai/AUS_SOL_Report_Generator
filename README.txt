Run WebScrapping.py inside 'Scripts\WebScrapping.py' and follow the instructions.

You can request the script to perform the following (three actions):

	1. To store the latest copy of the Skilled Occupation List(SOL) of Australia in the script's database(Data/Records):
		(Requires Internet)
		After running 'WebScrapping.py', the script first asks whether you want to store latest SOL.
		-If you want to then: Type "y" and press Enter key.
		-If not then: Type "n" and press Enter key.
		-If you want to exit the script: Type "e" and press Enter key.

	2. To generate SOL report(all occupations) from the script's database:
		(Works for both cases of internet connectivity and no internet connectivity)
		Only if you gave "n" to the first action then, it will ask you if you want to generate a report file inside Data folder. Performing this action will also perform the first action only when there is an internet connection.
		-If you want to then: Type "y" and press Enter key.
		-If not then: Type "n" and press Enter key.
		-If you want to exit the script: Type "e" and press Enter key.
		This action will generate an SOL report of all occupations between two desired dates from script's database and in case the script's database does not have SOL of the desired dates then, it will automatically choose dates nearest to it in its database and generate a report file which will include details like no changes, added occupations with its total number, removed occupations with its total number and all other occupations also.

	3. To generate up-to-date SOL report(of IT related occupations only)from the script's database:
		(Requires Internet)
		Only if you gave "n" to the second action then, it will ask you if you want to generate a report file inside Data folder.
		-If you want to then: Type "y" and press Enter key.
		-If not then: Type "n" and press Enter key.
		-If you want to exit the script: Type "e" and press Enter key.

	At last, the script asks if you want to continue. If entered "y" then the script will start from the first action and, "n" will end the script.	


This script has two interface:
	
	A. When internet connectivity is available:
		All three above actions can be performed.

	B. When there is no internet connection:
		Only the second action can be performed.	