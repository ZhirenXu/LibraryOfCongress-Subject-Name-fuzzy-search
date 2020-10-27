from bs4 import BeautifulSoup
from functions import DataSeperation
import urllib.request
import sys

nameSearchUrl = "https://id.loc.gov/search/?q=rdftype:Authority&q=memberOf:http://id.loc.gov/authorities/names/collection_LCNAF"
#change first q= to search
subjectSearch = "https://id.loc.gov/search/?q=memberOf:http://id.loc.gov/authorities/subjects/collection_LCSHAuthorizedHeadings"

def getNameSearchUrlPrefix():
    nameSearchPrefix = "http://id.loc.gov/search/?q="
    return nameSearchPrefix

def getNameSearchUrlSuffix():
    nameSearchSuffix = "&q=rdftype%3AAuthority&q=memberOf%3Ahttp%3A%2F%2Fid.loc.gov%2Fauthorities%2Fnames%2Fcollection_LCNAF"
    return nameSearchSuffix

def getSubjectSearchUrlPrefix():
    subjectSearchPrefix = "http://id.loc.gov/search/?q="
    return subjectSearchPrefix

def getSubjectSearchUrlSuffix():
    subjectSearchSuffix = "&q=memberOf%3Ahttp%3A%2F%2Fid.loc.gov%2Fauthorities%2Fsubjects%2Fcollection_LCSHAuthorizedHeadings"
    return subjectSearchSuffix

## Enter keywords in LOC's search page and pull first 10 results back
#  @param   *names
#           an *arg, typically contain a list of keywords
#  @return  nameData
#           a list contain lists which have raw name, correct name, url, perferred label and subdivision
def fuzzyNameSearch(*names):
    userChoice = 0
    i = 0
    # A list store several term dataclass
    nameUrlList = []
    htmlList = []
    termList = []
    # This is a list conatins list!
    dataList = []
    containerCluster = []
    nameData = []
    totalRecordNum = len(names[0])
    mappedRecord = {}
    print("\nSearch name terms in fuzzy mode...")
    print("Total number of record: ", totalRecordNum)
    for name in names[0][1:]:
        processedName = URI_escape(name)
        nameUrlList.append(getNameSearchUrlPrefix() + processedName + getNameSearchUrlSuffix())
    #can be optimized using multi-thread
    for url in nameUrlList:
        print("Opening Url: ", url)
        try:
            html = urllib.request.urlopen(url)
            htmlList.append(html)
        except HTTPError:
            print("Fail to open url: ", url)
            print("Press any key to exit")
            input()
            sys.exit(0)
    for html in htmlList:
        soup = BeautifulSoup(html, 'html.parser', from_encoding = 'utf-8')
        dataList.append(soup.find_all('tbody', attrs={'class': 'tbody-group'}))
    for data in dataList:
        if data == []:
            print("\nSorry, there is no result comes back from LOC's general search.")
            print("Term with no result: ", names[0][1:][i])
            nameData.insert(0, [names[0][0][i], names[0][1:][i], "null", "null", "null", "null"])
            mappedRecord[names[0][1:][i]] = -1
        else:
            containerCluster = DataSeperation.seperate(data)
            print("\n\nCurrent term: ", names[0][1:][i])
            if not (names[0][1:][i] in mappedRecord):
                userChoice = displayOption(containerCluster)
                mappedRecord[names[0][1:][i]] = userChoice
            else:
                userChoice = mappedRecord[names[0][1:][i]]
            #load list of data into a list
            if userChoice == -1:
                nameData.insert(0, [names[0][0][i], names[0][1:][i], "null", "null", "null", "null"])
            else:
                nameData.insert(0, [names[0][0][i], names[0][1:][i], containerCluster[userChoice - 1].title, containerCluster[userChoice - 1].LC_URI, containerCluster[userChoice - 1].concept, containerCluster[userChoice - 1].subdivision])
            containerCluster = []
        i = i + 1
    return nameData

## Enter keywords in LOC's search page and pull first 10 results back
#  @param   *subjects
#           an *arg, typically contain a list of keywords
#  @return  subjectData
#           a list contain lists which have raw subject, correct subject, url and perferred label
def fuzzySubjectSearch(*subjects):
    userChoice = 0
    i = 0
    # A list store several term dataclass
    subjectUrlList = []
    htmlList = []
    termList = []
    # This is a list conatins list!
    dataList = []
    #termContainer = []
    containerCluster = []
    subjectData = []
    totalRecordNum = len(subjects[0])
    mappedRecord = {}

    print("\nSearch subject terms in fuzzy mode...")
    print("Total number of record: ", totalRecordNum)
    for subject in subjects[0][1:]:
        processedSubject = URI_escape(subject)
        subjectUrlList.append(getSubjectSearchUrlPrefix() + processedSubject + getSubjectSearchUrlSuffix())
    #can be optimized using multi-thread
    for url in subjectUrlList:
        print("Opening Url: ", url)
        try:
            html = urllib.request.urlopen(url)
            htmlList.append(html)
        except HTTPError:
            print("Fail to open url: ", url)
            print("Press any key to exit")
            input()
            sys.exit(0)
    for html in htmlList:
        soup = BeautifulSoup(html, 'html.parser', from_encoding = 'utf-8')
        dataList.append(soup.find_all('tbody', attrs={'class': 'tbody-group'}))
    for data in dataList:
        if data == []:
            print("\nSorry, there is no result comes back from LOC's general search.")
            print("Term with no result: ", subjects[0][1:][i])
            subjectData.insert(0, [subjects[0][0][i], subjects[0][1:][i], "null", "null", "null", "null"])
            mappedRecord[subjects[0][1:][i]] = -1
        else:
            containerCluster = DataSeperation.seperate(data)
            print("\n\nCurrent term: ", subjects[0][1:][i])
            if not(subjects[0][1:][i] in mappedRecord):
                userChoice = displayOption(containerCluster)
                mappedRecord[subjects[0][1:][i]] = userChoice
            else:
                userChoice = mappedRecord[subjects[0][1:][i]]
            #load list of data into a list
            if userChoice == -1:
                subjectData.insert(0, [subjects[0][0][i], subjects[0][1:][i], "null", "null", "null", "null"])
            else:
                subjectData.insert(0, [subjects[0][0][i], subjects[0][1:][i], containerCluster[userChoice - 1].title, containerCluster[userChoice - 1].LC_URI, containerCluster[userChoice - 1].concept, containerCluster[userChoice - 1].subdivision])
            containerCluster = []
        i = i + 1
    return subjectData

## Display terms to let client choose
#  @param   cluster
#           A list of term data class
#  @return  choice
#           which num they choose
def displayOption(cluster):
    choice = 0

    print("\nPlease choose from following result, hit enter if no one is correct: \n")
    for term in cluster:
        print(term.num, "Title: ", term.title, "    ", "Vocabulary: ", term.vocabulary, "    ", "Concept: ", term.concept, "    ", "Subdivision: ", term.subdivision, "\n")
    print("Enter the number before each term: ", end = "")
    #empty input protection
    rawInput = input()
    #invalid input protection
    if len(rawInput) == 0:
        return -1;
    while int(rawInput) == 0 or int(rawInput) < -1 or int(rawInput) > len(cluster):
        print("The number you selected is invalid. Please type in number displayed.")
        print("If you want to exit the program press ctrl+c.")
        print("Enter the number before each term, hit enter if no one is correct: ", end = "")
        rawInput = input()
    choice = int(rawInput)

    return choice

##Process the initial name to fit url format
# @param    word
#           keyword for LOC name search
# @return   a processed word which can put in url without error
def URI_escape(word):
  return word.replace(' -- ', '--').replace(' ', '%20').replace(',', '%2C').replace("'","%27").replace('(', '%28').replace(')', '%29')
