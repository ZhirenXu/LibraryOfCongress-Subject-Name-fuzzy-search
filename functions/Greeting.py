import sys

## print program info
def showInfo():
    print("************************************************************")
    print("*   LibraryOfCongress Subject/Name Fuzzy Scrapper v1.1.0   *")
    print("*                  Author: Zhiren Xu                       *")
    print("*               published data: 10/27/20                   *")
    print("************************************************************")
    print("Check this repo to see Ruth's work: https://github.com/ruthtillman/subjectreconscripts")
    
## print exit message
# @param    fileOut
#           name of output file
def sysExit(fileOut):
    print("\nThe program is finished. The output file is: ", fileOut, " \n. It is located in the same folder with your main.py program. Press enter to exit.")
    key = input()
    sys.exit()
