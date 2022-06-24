How to run Report App:

Go to the "Report" file and inside of that file you will find a file named Reports that contains 2 files.
Go to the "Inputs_Report" and you will find 4 text files.


Input for Report:

- The "directi" file contains the address of the database within the current system. an example input for this file would be the following:

C:\\Users\\samueltaliaferro\\Desktop\\nameSearchArticles\\Sites_dataBase

As you can see the convention for writting the address is to write it as you would regularly see it in within file explorer but to replace
the single backslash "\" with a double backslash "\\". If no data-base exist in the given directory a new data-base will be created.


- The "input-sites" file contains a dictionary of all the sites you want to create a report for.

An example convention for the text that must be in this file is as follows:

{"SiteNameToSaveInData-Base": "SiteUrlToScrapeWithoutTheLastForwardSlash" , "siglo": "http://www.elsiglo.com.pa", "panamaamerica": "https://www.panamaamerica.com.pa","diaadia": "https://www.diaadia.com.pa"}

As you can see you write the site name that will be used to save the site in the database and the url separated by a colon within curly brackets:

{"SiteNameToSaveInData-Base": "SiteUrlToScrapeWithoutTheLastForwardSlash"}

then if you want to add more sites to scrape to the dictionary you just add them to the list and separate by comas:

{"SiteNameToSaveInData-Base": "SiteUrlToScrapeWithoutTheLastForwardSlash", "SiteNameToSaveInData-Base2": "SiteUrlToScrapeWithoutTheLastForwardSlash2"}


- The "input-names" contains the list of names that you want to search for the report.

An example convention for the text that must be in this file is as follows:

[name1, name2, name3]

As you can see you write the list within brackets and separate them with a coma and one space ", ". If the above convention is not followed
the app will not run.


- The "input-words" contains the list of words that you want to search for the report.

An example convention for the text that must be in this file is as follows:

[word1, word2, word3]

As you can see you write the list within brackets and separate them with a coma and one space ", ". If the above convention is not followed
the app will not run.


- The GuiReport app must be in the same directory that the "Reports" file is located for the app to run propperly.


- When the scrapper app is ran a Gui will ask you to input the range of dates to Report on. You can input the Dates manually 
with the following convention:

YYYY-MM-DD   

example:
2022-06-15

You can also enter the date range to scrape using a calendar that pops up when you press "DATE TO START SEARCH" and 
"DATE TO END SEARCH" buttons.


- To run the program you just press the "Create Report" Button.

- The program should run relatively fast if the date range is small and the names list is small but the run time will 
be exponentially slower if you have a long list of names and a long range to report on.

- When you run the program the Gui will not respond but as long as you see activity in the command line window that was opened 
you can be sure that the program is still running.

- If for any reason you need to cancel the program mid run you would just close the command line window that was opened with the program.


