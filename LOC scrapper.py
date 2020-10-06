from functions import Greeting
from functions import SimpleCSV
from functions import Run
import os

def main():
    inputCSV = ""
    outputCSV = ""
    isSearchName = True
    keyword = []
    result = []
    header = ["Input Term", "Title", "Vocabulary", "Concept", "Subdivision"]

    print("current directory: ", os.getcwd())
    #greeting
    Greeting.showInfo()
    #read from input, return rows in list, update search mode
    inputCSV = SimpleCSV.getCSVInput()
    outputCSV = SimpleCSV.getCSVOutput()
    keyword = SimpleCSV.readCSV(inputCSV)
    keyword.pop(0)
    isSearchName = Run.askSearchMode()
    #run process (precise->fuzzy->output), return a list contain lists of each row
    result = Run.processSerial(keyword, isSearchName)
    #write into output csv
    openedOut = open(outputCSV, 'w', encoding = 'utf-8',newline='')
    SimpleCSV.writeCSV(header, openedOut)
    for row in result:
        SimpleCSV.writeCSV(row, openedOut)
    #exit
    openedOut.close()
    Greeting.sysExit(outputCSV)
    
if __name__ == "__main__":
    main()
