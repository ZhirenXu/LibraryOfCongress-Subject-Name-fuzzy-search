import urllib.request
from bs4 import BeautifulSoup
from functions import FuzzySearch
import sys

def loadUrl(url):
    html = urllib.request.urlopen(url)
    return html

##main process of search in two mode
# @param    *argv
#           parameters, first is suppoose to be a list conatin search keyword
#           second is suppose to be a boolean value of search mode
#           True for name search, False for subject search
# @return   resultList
#           a list of correct name
def processSerial(*argv):
    resultList = []
    
    #name search mode
    if argv[1] == True:
        resultList = nameProcess(argv[0])
    #subject search mode
    elif argv[1] == False:
        resultList = subjectProcess(argv[0])
    print("\nkeyword search complete!")
    return resultList

## Name mode process
# @param    keywordList
#           a list conatin search keyword
# @return   result
#           a list contain lists which have raw name, correct name, url, perferred label and subdivision
def nameProcess(keywordList):
    fuzzyResult = []
    result = []
    failedResult = []
    
    print("\nSearch name terms in fuzzy mode...")

    fuzzyResult = FuzzySearch.fuzzyNameSearch(keywordList)
    return fuzzyResult

## Subject mode process
# @param    keywordList
#           a list conatin search keyword
# @return   result
#           a list contain lists which have raw name, correct name, url, perferred label and subdivision
def subjectProcess(keywordList):
    fuzzyResult = []
    result = []
    failedResult = []
    
    #failedResult = checkFailure(preciseResult, keywordList)
    fuzzyResult = FuzzySearch.fuzzySubjectSearch(keywordList)
    result = fuzzyResult
    return result
    
## Check if any precise search result is null.
## If true,delete it from search result and add to another list for fuzzySearch
## If isPrint is true, print user-friendly message
# @param    result
#           a list come from precise search, which have name/subject, url and perferred label
# @param    *terms
#           parameters, first is suppoose to be a list conatin search keyword
#           second is suppose to be a boolean value of search mode
#           True for name search, False for subject search
# @return   failed
#           a list contains all failed terms
def checkFailure(result, *terms):
    failed = []
    i = 0

    print("\nCheck null results...", end = "")
    for element in result:
        if "null" in element:
            failed.append(terms[0][i])
            i = i + 1     
    print("Done!")
    print("\nFailed: ")
    for element in failed:
        print(element)
         
    return failed

## merge results from two search mode together
# @param    precise
#           a list contain lists which have name/subject, url and perferred label
# @param    fuzzy
#           a list contain lists which have name/subject, url and perferred label
# @return   combinedResult
#           a list contain list which none of them are null
def mergeResult(precise, fuzzy):
    combinedResult = []
    length = len(fuzzy)
    isMatched = False
    
    #need re-design this 6/8
    for element in precise:
        isMatched = False
        term = element[0]
        if "null" in element:
            for item in fuzzy:
                if item[0] == term:
                    combinedResult.append(item)
                    isMatched = True
                    break
            if isMatched == False:
                combinedResult.append(element)
        else:
            combinedResult.append(element)
    return combinedResult

## ask user what search mode they perfer to run
# @return   searchMode
#           A boolean value, true for name search, false for subject search
def askSearchMode():
    print("Which search mode you perfer?")
    print("1. Name search (LCNAF)        2. Subject search (LCSH)")
    print("Enter the number before each term: ", end = "")
    #empty input protection
    rawInput = input()
    #invalid input protection
    while len(rawInput) == 0 or int(rawInput) < 1 or int(rawInput) > 2:
        print("The number you selected is invalid. Please type in number displayed.")
        print("If you want to exit the program press ctrl+c.")
        print("Enter the number before each term: ", end = "")
        rawInput = input()
    if int(rawInput) == 1:
        return True
    else:
        return False        
