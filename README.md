# Financial_Statement_Analyzer
  This is a small program that allow the user to crawl the financial statement (Balance Sheet, Statement of Comprehensive income, Statement of Cash Flow) of Taiwanese IPO firms, and utilize these datato do financial statement analysis. The packaged main program can be downloaded athttps://www.dropbox.com/s/63l31l6gxn7gpgv/financial_statement_analyzer.exe?dl=0. The main program provide some function to be called. The instruction can be prompt by command line (enter 1,2,3,4 or 5).  
* 0: Crawl financial statement
  * The program will ask how many period (1~3) the user want to analysis
  * Enter index/name
  * The program will ask the user if there is other firms to crawl in the analysis
* 1: Read financial statement
  * If there is existing financial statement file (.csv), the user can choose to read the data directly
* 2: Liquidity analysis
  * The program will print a dataframe containing multiple liquidity ratios, and ask the user whether to save the result.
* 3: Leverages and coverage analysis
  * The program will print a dataframe containing multiple leverage ratios, and ask the user whether to save the result.
* 4: Dupont analysis
  * The program will print a dataframe containing result of Dupont analysis, and ask the user whether to save the result.
* 5: Exist the program
