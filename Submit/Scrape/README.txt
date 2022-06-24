How to run Scrapper:

Go to the Scrape file and inside of that file you will find a file named Scrapper_inputs that contains 3 text files.

Input for Scrapper:

- The "directi" file contains the address of the database within the current system. an example input for this file would be the following:

C:\\Users\\samueltaliaferro\\Desktop\\nameSearchArticles\\Sites_dataBase

As you can see the convention for writting the address is to write it as you would regularly see it in within file explorer but to replace
the single backslash "\" with a double backslash "\\". If no data-base exist in the given directory a new data-base will be created.


- The "java-list" contains the list of sites that must be rendered in java. To know if a site is rendered in java one must inspect the sites 
elements but for the panamanian news site the only java rendered site I found was la prensa.

An example convention for the text that must be in this file is as follows:

[prensa, site2, site3]

As you can see you write the list within brackets and separate them with a coma and one space ", ". If the above convention is not followed
the app will not run.


- The "sites-dict" file contains a dictionary of all the sites you want to scrape.

An example convention for the text that must be in this file is as follows:

{"SiteNameToSaveInData-Base": "SiteUrlToScrapeWithoutTheLastForwardSlash" , "siglo": "http://www.elsiglo.com.pa", "panamaamerica": "https://www.panamaamerica.com.pa","diaadia": "https://www.diaadia.com.pa"}

As you can see you write the site name that will be used to save the site in the database and the url separated by a colon within curly brackets:

{"SiteNameToSaveInData-Base": "SiteUrlToScrapeWithoutTheLastForwardSlash"}

then if you want to add more sites to scrape to the dictionary you just add them to the list and separate by comas:

{"SiteNameToSaveInData-Base": "SiteUrlToScrapeWithoutTheLastForwardSlash", "SiteNameToSaveInData-Base2": "SiteUrlToScrapeWithoutTheLastForwardSlash2"}


- The GuiScrapper app must be in the same directory that the Scrapper_inputs file is located for the app to run propperly.


- When the scrapper app is ran a Gui will ask you to input the range of dates to scrape. You can input the Dates manually 
with the following convention:

YYYY-MM-DD   

example:
2022-06-15

You can also enter the date range to scrape using a calendar that pops up when you press "DATE TO START SCRAPING" and 
"DATE TO END SCRAPING" buttons.

- If you enter the word "now" in the "DATE TO START SCRAPING" field you will scrape the articles that are currently 
in the list of sites that where given.

- To run the program you just press the "Scrape Range" Button.

- The program should run relatively fast if the sites that will be scraped are not java rendered but if you give a java rendered
 site to be scraped then the program will run much slower but it should still work fine.

- When you run the program the Gui will not respond but as long as you see activity in the command line window that was opened 
you can be sure that the program is still running.

- If for any reason you need to cancel the program mid run you would just close the command line window that was opened with the program.


