'''
Financial Statement Analysis: Company
Author: hanktsai404
Created at 03.05.2021
'''
import requests
from bs4 import BeautifulSoup
import json
import random
import pandas as pd
import numpy as np
import time, datetime
import os
from io import StringIO
import matplotlib.pyplot as plotter

YEAR = datetime.datetime.now().year

class company():
    def __init__(self, index: str, name: str):
        self.index = index
        self.name = name
        self.stock_path = os.getcwd() + "\\" + str(self.index) + "_" + self.name
        self.fs_dict = dict()
        if not os.path.isdir(self.stock_path):
            os.mkdir(self.stock_path)
    
    def crawl_fs(self, year = YEAR - 1):
        '''Crawl the financial statements'''
        fs_url = "https://mops.twse.com.tw/server-java/t164sb01?step=1"+"&"+"CO_ID="+str(self.index)+"&SYEAR="+str(year)+"&SSEASON=4&REPORT_ID=C"
        # print(fs_url)
        fs_web = requests.get(fs_url)
        fs_web.encoding = "big5"
        print("check")  # sucessfully enter the website
        fs_datas = pd.read_html(StringIO(fs_web.text))
        time.sleep(random.randint(1, 5))
        bs_sheet = fs_datas[0]
        bs_sheet.columns = ["Code", "Title", str(year), str(year-1)]
        statement_of_CI = fs_datas[1]
        statement_of_CI.columns = ["Code", "Title", str(year), str(year-1)]
        statement_of_CF = fs_datas[2]
        statement_of_CF.columns = ["Code", "Title", "In"+str(year), "In"+str(year-1)]
        
        self.fs_dict[year] = {'bs_sheet': bs_sheet, 'statement_of_CI': statement_of_CI, 'statement_of_CF': statement_of_CF}
    
    def write_fs_to_csv(self):
        for key in self.fs_dict.keys():
            for sub_key in self.fs_dict[key].keys():
                target_csv = open(self.stock_path + "\\" + str(sub_key) + str(key) + ".csv", "w", newline="", encoding="UTF-8")
                self.fs_dict[key][sub_key].to_csv(target_csv)
                target_csv.close()

if __name__ == "__main__":
    FIH = company("2707", "FIH")
    FIH.crawl_fs(2020)
    FIH.crawl_fs(2019)
    FIH.write_fs_to_csv()