# LibraryOfCongress-Subject-Name-Fuzzy-Scrapper  

A script that can scrapes terms from LOC for library use.

User can choose search mode and generate a csv file as output.
Currently support LCNAF and LCSH searching.
The script will read keywords from input file and display candidates for expected term. There are up to 15 candidates.
If there are terms that cannot return precise search result, the output for that keywords will be all null except its name.
If all input terms failed, the output csv will only have header.

## Prerequisites:  

   Run in Windows 10 environment. 
   
   Python ver. 3.8 or higher, other version has not been tested. 
   
   Required Package: 
      
      BeautifulSoup 
	   
      
   If not installed, please open CMD, go to the path of id scraper folder, then type following command:
   
	  pip install -r dependencies.txt  

   If dependencies.txt doesn't exist or command above has failure, try manually install dependencies by tying following command:
      
      pip install bs4  
	  
	
## Instruction
1. put csv file which contain name terms or subject terms in the same folder as the LOC Scrapper. CSV file SHOULD NOT conatin header.
2. run 'LOC fuzzy search.py'  
3. follow instructions on display  