To settup the scrapper and reporter you must first place the "Sites_dataBase" file in a shared directory. then you need to update
the "directi" foled in both the scapper and the reporter inputs so they have access to the database. once both apps have access
to the database directory you can run either app from any directory you want. you just need to keep the app with its respective files 
in the same folder they are currently in. that would be the "Report" and the "Scrape" folder. as I said before the database can be placed
wherever you want as long as you update the directi input for both apps.

if for any reason you decide to make a change to the source code you can transform it into an app by running pyinstaller in the 
CMD. You can do so as follows:

pyinstaller --onefile GuiScrapper.py

and

pyinstaller --onefile GuiReport.py
