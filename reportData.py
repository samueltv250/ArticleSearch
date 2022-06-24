from pathlib import Path
from datetime import *
import os
import xlsxwriter
import time
import re
import pickle

import numpy as np
import json


def getExistingDatesOfSite(date1, date2, site, databasePath):

    startDate = date(int(date1[0:4]),int(date1[5:7]), int(date1[8:10]))
    
    endDate = date(int(date2[0:4]),int(date2[5:7]), int(date2[8:10]))
    
    existingDates = []
    directi = Path(databasePath+"/"+site+"/")
    for file in os.listdir(directi)[1:]:
        if file not in ["urlsqueue.txt","urlsqueue.pickle",".DS_Store" ]:
#            print(file)
            fdate = date(int(file[0:4]),int(file[5:7]), int(file[8:10]))

            if fdate >= startDate and fdate <= endDate:
                existingDates.append(file)
    return existingDates
        
        
        

def searchString2(names, words, data, url,date):

    

    outputforfile = []
    for name in names:
        temp = []
        tempwords = []

        if name.lower() in data:
        
        
        
        
            temp.append(name)
#           cleaning Urls os they are accesible
            nurl = url.replace("https@@@", "https://")
            nurl = nurl.replace("@", "/").replace("[","?" ).replace("]","*" )
            date = str(date)
            nurl = nurl.replace(".pickle", "")
            temp.append(nurl)
            for word in words:
                if word.lower() in data:
                    tempwords.append(word)
            temp.append(tempwords)
            temp.append(data)
            
            tokenizedData = re.split('\n| |  |\(|\)',data)
            moneyVal = []
#            finding monetary values
            for tok in range(len(tokenizedData)):
                if len(tokenizedData[tok])> 0 and tokenizedData[tok][0] == "$":
                    moneyNow = str(tokenizedData[tok])
                
                    if tok < len(tokenizedData)-1 and len(tokenizedData[tok+1]) >2 and (tokenizedData[tok+1][0].lower() == 'm' or tokenizedData[tok+1][0].lower() == 'b'):
                        moneyNow += " " +str(tokenizedData[tok+1])
                    moneyVal.append(moneyNow)
                            
            
             
            temp.append(moneyVal)
            temp.append(date)
            outputforfile.append(temp)

    return outputforfile
    


def winapi_path(dos_path, encoding=None):
    if (not isinstance(dos_path, str) and
        encoding is not None):
        dos_path = dos_path.decode(encoding)
    path = os.path.abspath(dos_path)
    if path.startswith(u"\\\\"):
        return u"\\\\?\\UNC\\" + path[2:]
    return u"\\\\?\\" + path


    
def searchString(sitelist, date1, date2, names, words, databasePath):

    finalOutPuts = []
#    iterating through sites


    for site in sitelist:
        existingDates = getExistingDatesOfSite(date1, date2, site,databasePath)
        
        for date in existingDates:
            directi = Path(databasePath+"\\"+site+"\\"+date+"\\")
#            iterating through every date within the range in the site database
            for file in os.listdir(directi)[1:]:
                if file != "urlsqueue.pickle" and file != ".DS_Store":
                    path = winapi_path(os.path.join(databasePath, site, date, file))
                    filetoop = directi /file
                    
                    
                    with open(path,"rb") as Text:
                        currdat = pickle.load(Text)
                    
                    
                    currdat = currdat.lower()

                    
           
                    outputforurl = searchString2(names, words, currdat, file,date)
     
                    for op in outputforurl:
                        finalOutPuts.append(op)
                        
                   
                    
    return finalOutPuts
                
          
#       group the outputs so that each row is only for a name containing all its found urls in one cell
def reOrderOutput(finalOutPuts):

    Columnvers = list(zip(*finalOutPuts))
    
    if(len(Columnvers)!=0):
        dupl = Columnvers[0]
        dicttion = dict.fromkeys(dupl)
        deduplicat = list(dicttion)
        
        orderedoutp = []
        for op in deduplicat:
            temp = []
            tempurls = []
            tempwords = []
            temp.append(op)
            
            for po in finalOutPuts:
                if po[0] == op:
                    tempurls.append(po[1])
                    for wo in po[2]:
                        tempwords.append(wo)
            dicttion = dict.fromkeys(tempwords)
            deduplicatwords = list(dicttion)
            temp.append(deduplicatwords)
            
            temp.append(tempurls)
            orderedoutp.append(temp)
        
      
                        
        return orderedoutp
                
          
          
          
          

                
#save everything to a excel separately
def saveExcelBasic(listofoutputs):
    #create file(workbook) and worksheet
    e = time.strftime("%Y%m%d-%H%M%S")
  
    
    
    directi = Path("Reports"+"/"+"Outputs_Report"+"/"+"Basic"+"/")
    if not os.path.exists(directi):
        os.mkdir(directi)
    file = "outputReportBasic_"+e+".xlsx"
    filetoop = directi /file
    
    outWorkbook = xlsxwriter.Workbook(filetoop)
    outSheet = outWorkbook.add_worksheet()
    excelColumn = list(zip(*listofoutputs))
  
    #declare data
    if len(excelColumn) == 6:
        words = excelColumn[0]
        urls = excelColumn[1]
        texts = excelColumn[2]
        words2 = excelColumn[3]
        moneyMult = excelColumn[4]
        date = excelColumn[5]
        cell_format = outWorkbook.add_format({'bold': True, 'bg_color':'blue', 'font_color':'white','border': True})
        cell_format2 = outWorkbook.add_format({'bg_color':'white','border': True,'text_wrap' : True})

        outSheet.write("A1","Names",cell_format)
      
        outSheet.write("B1","Date",cell_format)
        outSheet.write("C1","Words",cell_format)
        outSheet.write("D1","Text in article",cell_format)
        outSheet.write("E1","Monetary value in article",cell_format)
        outSheet.write("F1","Url",cell_format)
        
        outSheet.set_column(3, 3,150)
        outSheet.set_column(0, 0,30)
        outSheet.set_column(2, 2,30)
        outSheet.set_column(5, 5,100)
        outSheet.set_column(1, 1,15)
        
        outSheet.set_column(4, 4,30)
        for item in range(len(words)):
            outSheet.write(1+item, 0,str(words[item]),cell_format2)


            outSheet.write(1+item, 1,str(date[item]),cell_format2)
            
            

            outSheet.write(1+item, 5,str(urls[item]),cell_format2)
            
            
            

            STR2 = ""
            for oo in texts[item]:
                STR2 += oo+"\n"
            if len(texts[item]) != 0:
                outSheet.write(1+item, 2,STR2 ,cell_format2)
            else:
                outSheet.write(1+item, 2,"No words found related to this person",cell_format2)
                

            STR2 = ""

            for oo in moneyMult[item]:
                STR2 += oo+"\n"
            if len(moneyMult[item]) != 0:
                outSheet.write(1+item, 4,STR2 ,cell_format2)
            else:
                outSheet.write(1+item, 4,"No monetary value found related to this article",cell_format2)


            
        for item in range(len(words)):
            outSheet.write(1+item, 3,str(words2[item]),cell_format2)

        
        
    outWorkbook.close()
    
    
    
    
def saveExcelnwRemoved(listofoutputs):
    #create file(workbook) and worksheet
    e = time.strftime("%Y%m%d-%H%M%S")
  
    
    
    directi = Path("Reports"+"/"+"Outputs_Report"+"/"+"OnlyWords"+"/")
    if not os.path.exists(directi):
        os.mkdir(directi)
    file = "outputReportOnlyWords_"+e+".xlsx"
    filetoop = directi /file
    
    outWorkbook = xlsxwriter.Workbook(filetoop)
    outSheet = outWorkbook.add_worksheet()
    nlist = []
    
    for p in range(len(listofoutputs)):

        if len(listofoutputs[p][2]) != 0:
            nlist.append(listofoutputs[p])
            
    listofoutputs = nlist
    
    excelColumn = list(zip(*listofoutputs))
  
    #declare data
    if len(excelColumn) == 6:
        words = excelColumn[0]
        urls = excelColumn[1]
        texts = excelColumn[2]
        words2 = excelColumn[3]
        moneyMult = excelColumn[4]
        date = excelColumn[5]
        cell_format = outWorkbook.add_format({'bold': True, 'bg_color':'blue', 'font_color':'white','border': True})
        cell_format2 = outWorkbook.add_format({'bg_color':'white','border': True,'text_wrap' : True})

        outSheet.write("A1","Names",cell_format)
      
        outSheet.write("B1","Date",cell_format)
        outSheet.write("C1","Words",cell_format)
        outSheet.write("D1","Text in article",cell_format)
        outSheet.write("E1","Monetary value in article",cell_format)
        outSheet.write("F1","Url",cell_format)
        
        outSheet.set_column(3, 3,150)
        outSheet.set_column(0, 0,30)
        outSheet.set_column(2, 2,30)
        outSheet.set_column(5, 5,100)
        outSheet.set_column(1, 1,15)
        
        outSheet.set_column(4, 4,30)
        for item in range(len(words)):
            outSheet.write(1+item, 0,str(words[item]),cell_format2)


            outSheet.write(1+item, 1,str(date[item]),cell_format2)
            
            

            outSheet.write(1+item, 5,str(urls[item]),cell_format2)
            
            
            

            STR2 = ""
            for oo in texts[item]:
                STR2 += oo+"\n"

            outSheet.write(1+item, 2,STR2 ,cell_format2)

                

            STR2 = ""

            for oo in moneyMult[item]:
                STR2 += oo+"\n"
            if len(moneyMult[item]) != 0:
                outSheet.write(1+item, 4,STR2 ,cell_format2)
            else:
                outSheet.write(1+item, 4,"No monetary value found related to this article",cell_format2)


            
        for item in range(len(words)):
            outSheet.write(1+item, 3,str(words2[item]),cell_format2)

        
        
    outWorkbook.close()


#save ecerything to a excel with the informating for each name joined
def saveExcelJoined(listofoutputs):
    #create file(workbook) and worksheet
    e = time.strftime("%Y%m%d-%H%M%S")
  
    
    directi = Path("Reports"+"/"+"Outputs_Report"+"/"+"Joined"+"/")
    if not os.path.exists(directi):
        os.mkdir(directi)
    file = "outputReportJoined_"+str(e)+".xlsx"
    filetoop = directi /file
                    
    
    outWorkbook = xlsxwriter.Workbook(filetoop,options ={'strings_to_urls' : False})
    outSheet = outWorkbook.add_worksheet()

    #add each website to a data base and mark it with date and time. then I will be able to give it a list to search for a specific time frame. also give a list of key works and mark the names that appear with the key words from the list if they also appear.
    #add each new article url to a list so that I only have to render each article once
    #pull everything from a day by saving each wensites urls for articles in a list stored in a dict with key (site-date)
    
    
    
#    formating cells
    cell_format = outWorkbook.add_format({'bold': True, 'bg_color':'blue', 'font_color':'white','border': True})
    cell_format2 = outWorkbook.add_format({'bg_color':'white','border': True,'text_wrap' : True})
    if(listofoutputs!=None):
        
        excelColumn = list(zip(*listofoutputs))

        #declare data
        if len(excelColumn) == 3:
        
            words = excelColumn[0]
          
            urls = excelColumn[1]
            texts = excelColumn[2]
            



            outSheet.write("A1","Names",cell_format)
            outSheet.write("B1","Words",cell_format)
            outSheet.write("C1","Urls",cell_format)
            outSheet.set_column(2, 2,150)
            outSheet.set_column(0, 1,30)
            for item in range(len(words)):
                
                outSheet.write(1+item, 0,str(words[item]),cell_format2)

   
                STR2 = ""
                for oo in texts[item]:
                    STR2 += oo+"\n"
                outSheet.write(1+item, 2,STR2,cell_format2)
                
        
                STR2 = ""
                for oo in urls[item]:
                    STR2 += str(oo)+"\n"
                if len(urls[item]) != 0:
                    outSheet.write(1+item, 1,STR2,cell_format2)
                else:
                    outSheet.write(1+item, 1,"No words found related to this person",cell_format2)
        outWorkbook.close()






#words = ["Narcotrafico", "Lavado","Droga","Banco","Robo","Coima","Muerto","Robado","Disparo","Trafico","Presidente","Crimen","Condenad"]
#
#names = ["Tito Afú","Academia","Panama Paper","Ricardo Martinelli","Nito Cortizo","Joe Biden","Obama","Taliaferro", "Heard","Covid"]
def searchAndReport(start,end):

#    start = input("Enter start Date as (YYYY-MM-DD)  :")
#    end = input("Enter end Date as (YYYY-MM-DD)    :")
    
    directi = Path("Reports"+"/"+"Inputs_Report"+"/")


    
    
    
    
    filename = "input-names.txt"
    filetoop = directi /filename
    with open(filetoop,"r") as fp:
        names = fp.read()
        namesn = names.strip('][').split(', ')
        

    filename = "input-sites.txt"
    filetoop = directi /filename
    with open(filetoop,"r") as fp:
        sites = fp.read()
        sites = json.loads(sites)

    filename = "input-words.txt"
    filetoop = directi /filename
    with open(filetoop,"r") as fp:
        words = fp.read()
        wordsn = words.strip('][').split(', ')
        
  
        
        
    sitesn = []
    for site in sites:
        sitesn.append(site.replace("\n",""))




    print("Searching the following names and words:")
    print("--------------------------------------------------------------------------------\n")
    print(namesn)
    print(wordsn)
    print("In the following sites:")
    print("--------------------------------------------------------------------------------\n")
    print(sitesn)
    print("From "+start+" to "+end)
    print("--------------------------------------------------------------------------------\n")






    filename = "directi.txt"
    filetoop = directi /filename
    with open(filetoop,"r") as fp:
        databasePath = str(fp.read())
        
        
        









    #preparing data to export to excel
    outpp = searchString(sitesn,str(start), str(end), namesn, wordsn,databasePath)
    ordered = reOrderOutput(outpp)



    #saving to both excel files
    saveExcelBasic(outpp)
    saveExcelnwRemoved(outpp)
    saveExcelJoined(ordered)
    print("Finish Search and created reports")
    
    return "Created Report from " +start+" to "+ end





#searchAndReport()
