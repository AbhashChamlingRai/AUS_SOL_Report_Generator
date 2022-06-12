First, run Del_Reports.py inside 'Scripts' directory.
Then, run WebScrapping.py inside 'Scripts' directory and follow the instructions.

You can request the script to perform the following (three actions):

	1. To store the latest copy of the Skilled Occupation List(SOL) of Australia in the script's database(Data/Records):
		(Requires Internet)
		After running 'WebScrapping.py', the script automatically stores latest SOL of current date into its database only if there is an internet connection.

	2. To generate SOL report(all occupations) from the script's database:
		(Works for both cases of internet connectivity and no internet connectivity)
		After completion of the first action(by running 'WebScrapping.py') or if the SOL of the current date allready exists in the database then, the script will ask you if you want to generate a report file inside Data folder.
		This action will generate an SOL report of all occupations between two desired dates from script's database and in case the script's database does not have SOL of the entered dates then, it will automatically choose dates nearest to it in its database to generate report file.
		So, you can only get latest SOL report if there is an internet connection.
		Depending on the conditions, the script will create a report file which will include details like:
			1. No changes with all the current occupation present in the latest SOL.
			B. Added occupations with its total number and all the current occupation present in the latest SOL.
			C. Removed occupations with its total number and all the current occupations present in the latest SOL.
			D. Both added as well as removed occupations with its total number and all the current occupations present in the latest SOL.

				---If you want to perform this action then:     Type "y" and press Enter key.
				---If not then: 				Type "n" and press Enter key.
				---If you want to exit the script: 		Type "e" and press Enter key.

	3. To generate latest SOL report(of IT related occupations only)from the script's database:
		(Works for both cases of internet connectivity and no internet connectivity)
		Only if you gave "n" to the second action then, script will ask you if you want to generate another report file inside Data folder.
		If there is an internet connection then, you will the latest information related to IT occupations in SOL of Australia.
		If there is no internet connection then, you will get a report of IT occupations from the most recently stored SOL in the databse.

				---If you want to perform this action then: 	Type "y" and press Enter key.
				---If not then: 				Type "n" and press Enter key.
				---If you want to exit the script: 		Type "e" and press Enter key.

	At last, the script asks if you want to continue. If entered "y" then the script will start from the first action and, "n" will end the script.	


This script has two interface:
	
	A. When internet connectivity is available:
		All three above actions can be performed.

	B. When there is no internet connection:
		Only the second and the third action can be performed.	