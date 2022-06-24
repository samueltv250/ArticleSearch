from requests_html import HTMLSession
import concurrent.futures
import queue
from pathlib import Path
import os
import sys
import time
import pickle
from datetime import date, timedelta, datetime
import re
import json



keepInQueue = 1500
render = False

QUEUE = queue.Queue()
concurrentSessions = 4
listOfExplored = []
dictOfText = {}






def getUrlsWayBack(Date,uurl,render,site,databasePath):
    stttr = "https://web.archive.org/web/"+str(Date)[0:4]+str(Date)[5:7]+str(Date)[8:10]+"/"+uurl
    urls = []
    session = getSession()
    try:
    
        response = session.get(stttr)
        
        if render == True:
            print("rendering")
            response.html.render(timeout=30)
        directi = Path(databasePath+"\\"+site+"\\"+str(Date)+"\\")
  
        if not os.path.exists(directi):
            os.mkdir(directi)
  
            
        response.raise_for_status()
        
        for x in response.html.absolute_links:
                urls.append(x)
    except:
        print("requiring")
        try:
        
            response = session.get(stttr)
            
            if render == True:
                print("rendering")
                response.html.render(timeout=30)
            directi = Path(databasePath+"\\"+site+"\\"+str(Date)+"\\")
      
            if not os.path.exists(directi):
                os.mkdir(directi)
      
                
            response.raise_for_status()
            
            for x in response.html.absolute_links:
                    urls.append(x)
        except Exception as e:
            print(e)

    
    finally:
        freeSession(session)
    return urls
    
    

def getUrlsToday(Date,uurl,render,site,databasePath):
    stttr = uurl
    urls = []
    session = getSession()
    try:
        response = session.get(stttr)
        if render == True:
            print("rendering")
            response.html.render(timeout=30)
        directi = Path(databasePath+"/"+site+"/"+str(Date)+"/")
  
        if not os.path.exists(directi):
            os.mkdir(directi)
  
            
        response.raise_for_status()
        
        for x in response.html.absolute_links:
                urls.append(x)
    finally:
        freeSession(session)
    return urls
    
    
    



def makeSessions(site,javaRendered):
    global concurrentSessions
    global render

    render = False
    concurrentSessions = 4
    
    if site in javaRendered:
        render = True
        concurrentSessions = 1
    for _ in range(concurrentSessions):
        QUEUE.put(HTMLSession())


def cleanup():
    while True:
        try:
            getSession(False).close()
        except queue.Empty:
            break


def getSession(block=True):
    return QUEUE.get(block=block)


def freeSession(session):
    if isinstance(session, HTMLSession):
        QUEUE.put(session)





def processURL(url,date,site,render, isToday):
    global listOfExplored
    global dictOfText
    
    if isToday == False:
        urltosearch = url[43:]
    else:
        urltosearch = url
    print(urltosearch)
    session = getSession()
    try:
        
        if urltosearch not in listOfExplored:
        
            response = session.get(url)
            response.raise_for_status()
            if render == True:
                print("Rendering: "+url)
                response.html.render(timeout=30)
            
            
            
            content = response.html.find('p')#find all text in website
            
  
            
            addToTxtQueue(urltosearch)
            
            textofart = ""
            for p in content:
                textofart+=p.text + " "
            
            dictOfText[url] = textofart
        else:
            print("Already extracted: "+ url)
            


    except Exception as e:
        print(e)
        
    finally:

        freeSession(session)
def winapi_path(dos_path, encoding=None):
    if (not isinstance(dos_path, str) and
        encoding is not None):
        dos_path = dos_path.decode(encoding)
    path = os.path.abspath(dos_path)
    if path.startswith(u"\\\\"):
        return u"\\\\?\\UNC\\" + path[2:]
    return u"\\\\?\\" + path



def extractFromWayBack(site,uurl,date,isToday,javaRendered,databasePath):
    global listOfExplored
    global dictOfText
    global render
    try:
        

        
    

        makeSessions(site,javaRendered)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            directi = Path(databasePath+"\\"+site+"\\")
            filename = "urlsqueue.pickle"
            filetoop = directi / filename
            listOfExplored = []
            
            if not os.path.exists(directi):
                os.mkdir(directi)
            if not os.path.exists(filetoop):
                with open(filetoop,"wb") as urlQueue:
                    pickle.dump(["Hi"],urlQueue)
                    print("Creating file: "+str(filetoop))
                    

            with open(filetoop,"rb") as urlQueue:
                listOfExplored = pickle.load(urlQueue)
               
            
            
            dictOfText = {}
            

            if isToday == False:
                futures = [executor.submit(processURL, url,date,site,render, isToday) for url in getUrlsWayBack(date,uurl,render,site,databasePath)]
            else:
                futures = [executor.submit(processURL, url,date,site,render, isToday) for url in getUrlsToday(date,uurl,render,site,databasePath)]
            

                
     
            for _ in concurrent.futures.as_completed(futures):
                pass
                

            
            
            
            
            with open(filetoop,"wb") as urlQueue:
                pickle.dump(listOfExplored,urlQueue)
                print("Dumped succesfully using "+str(concurrentSessions)+ " concurrent sessions")
      
            
            
            
            if isToday == True:
                for key in dictOfText:
                    

                    urlll = str(key).replace(":","@" ).replace("/","@" ).replace("?","[" ).replace("*","]" )
                    directi = Path(databasePath+"\\"+site+"\\"+str(date)+"\\")
              
                    filename = urlll+".pickle"
                    
                    if not os.path.exists(directi):
                        os.mkdir(directi)
                    path = winapi_path(databasePath+"\\"+site+"\\"+str(date)+"\\"+ urlll+".pickle")
                    
                    
                    filetoop = directi / filename
                    with open(path,"wb") as TXTQUEUE:
                        pickle.dump(dictOfText[key],TXTQUEUE)
            else:
                for key in dictOfText:
                    
#                    must fix so the files get saved in their respective dates.
                    urlll = str(key).replace(":","@" ).replace("/","@" ).replace("?","[" ).replace("*","]" )
                    directi = Path(databasePath+"\\"+site+"\\"+str(urlll)[28:32]+"-"+str(urlll)[32:34]+"-"+str(urlll)[34:36]+"\\")


              
                    filename = urlll+".pickle"
                    
                    if not os.path.exists(directi):
                        os.mkdir(directi)
                    path = winapi_path(databasePath+"\\"+site+"\\"+str(urlll)[28:32]+"-"+str(urlll)[32:34]+"-"+str(urlll)[34:36]+"\\"+ urlll+".pickle")
                    
                    
                    filetoop = directi / filename
                    with open(path,"wb") as TXTQUEUE:
                        pickle.dump(dictOfText[key],TXTQUEUE)
    except Exception as e:
        print(e)
            
    finally:

        cleanup()
        
        
        
        
def addToTxtQueue(url):
    global listOfExplored
    global dictOfText
    
    if len(listOfExplored) < keepInQueue:
        listOfExplored.append(url)
    else:
        listOfExplored.pop(0)
        listOfExplored.append(url)



def dateRange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)




def storeFromDates(start_date, end_date, site,sites,isToday,javaRendered,databasePath):
 


    for single_date in dateRange(start_date, end_date):
        print(single_date.strftime("%Y-%m-%d"))
 
        extractFromWayBack(site,sites[site],single_date.strftime("%Y-%m-%d"),isToday,javaRendered,databasePath)
        
            
def getData(start,end):

    isToday = False
    today = date.today()

#    start = input("Enter start Date as (YYYY-MM-DD)  :")

    if start.lower() == "now":
        isToday = True
        start_date = today
        end_date = today + timedelta(days=1)
        
    else:
        start_date = date(int(start[0:4]), int(start[5:7]), int(start[8:10]))


    if isToday == False:
#        end = input("Enter end Date as (YYYY-MM-DD)    :")
        if end.lower() == "now":
            end_date = today
        else:
            end_date = date(int(end[0:4]), int(end[5:7]), int(end[8:10]))



    direct = Path("Scrapper_inputs"+"/")



    filename = "directi.txt"
    filetoop = direct /filename
    with open(filetoop,"r") as fp:
        databasePath = str(fp.read())
        
        
        




    filename = "sites-dict.txt"
    filetoop = direct /filename
    with open(filetoop,"r") as fp:
        sites = fp.read()
        sites = json.loads(sites)






    filename = "java-list.txt"
    filetoop = direct /filename
    with open(filetoop,"r") as fp:
        javaRendered1 = fp.read()
        javaRendered = javaRendered1.strip('][').split(', ')
        




    if isToday == True:
        for sit in sites:
            print(str(today)+"   "+str(sit))
            storeFromDates(start_date, end_date, sit,sites,isToday,javaRendered,databasePath)
    else:
        for sit in sites:
            print(str(start_date)+"  "+str(end_date)+"  "+str(sit))
            storeFromDates(start_date, end_date, sit,sites,isToday,javaRendered,databasePath)
    
    return "scrped from "+str(start_date)+" to "+str(end_date)



