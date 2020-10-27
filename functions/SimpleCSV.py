import csv
import sys

##open csv file and read handler link, store in a list
# @param    csvIn
#           input file name and a boolean for search mode
# @return   dataList
#           a list contain names/subject that need to be scraped
def readCSV(csvIn):
    dataList = []
    urlList = []
    hasRunOnce = False
    columnNum = 0
    
    #try:
    inFile = open(csvIn, 'r', encoding = 'utf-8')
    csvReader = csv.reader(inFile, delimiter=',')
    for row in csvReader:
        if not hasRunOnce:
            print("\nwhich column you want to use as input? The column number START FROM 0.")
            print("For example, if data is in colomn 2, type 1.")
            print("Enter column number: ", end = "")
            columnNum = int(input())
            hasRunOnce = True
        try:
            urlList.append(row[0])
            dataList.append(row[columnNum])
        except:
            print("Your may enter an invalid column Num (too big or smaller than 0). Run the script again.")
            sys.exit()
    #get rid of header
    urlList.pop(0)
    dataList.pop(0)
    dataList.insert(0, urlList)
    print ("\nOpen input CSV success.")

    return dataList

##write category and data into csv file
# @param    dataList
#           a list contains data
# @param    outputFile
#           output File pointed by user, opened
def writeCSV(dataList, outputFile):
    try:
        csvWriter = csv.writer(outputFile)
        csvWriter.writerow(dataList)
        print("Write this row into CSV success.")
    except:
        print("Fail to write into CSV!")

##get input CSV file name
# @return       fileIn
#               Input CSV file
def getCSVInput():
    print("Please enter csv file name with .csv. \nThe file must in the same folder with your main.py program: ")
    fileIn = input()
    #add typo protection
    while ".csv" not in fileIn:
        print("No .csv detected in fileName. Do you want to type the name again?")
        print("If you want to exit please press enter.")
        print("File Name: ", end = '')
        fileIn = input()
        if len(fileIn) == 0:
            sys.exit()

    return fileIn

##get output CSV file name
# @return       fileOut
#               Output CSV file
def getCSVOutput():
    print("Please enter output file name (with .csv): ")
    fileOut = input()
    while ".csv" not in fileOut:
        print("No .csv detected in fileName. Do you want to type the name again?")
        print("If you want to exit please press enter.")
        print("File Name: ", end = '')
        fileOut = input()
        if len(fileOut) == 0:
            sys.exit()

    return fileOut
    
