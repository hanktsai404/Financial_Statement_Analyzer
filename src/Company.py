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
from tqdm import tqdm

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
        if year == 2018:
            self.fs_dict[year] = self.fs_dict[2019]
        else:
            fs_url = "https://mops.twse.com.tw/server-java/t164sb01?step=1"+"&"+"CO_ID="+str(self.index)+"&SYEAR="+str(year)+"&SSEASON=4&REPORT_ID=C"
            # print(fs_url)
            fs_web = requests.get(fs_url)
            fs_web.encoding = "big5"
            # print("check")  # sucessfully enter the website
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
    
    def read_fs_from_csv(self, period: int):
        self.fs_dict = dict()
        for i in range(period):
            key = YEAR-1-i
            bs_sheet = pd.read_csv(self.stock_path + "\\" + "bs_sheet" + str(key) + ".csv", encoding="UTF-8")
            statement_of_CI = pd.read_csv(self.stock_path + "\\" + "statement_of_CI" + str(key) + ".csv", encoding="UTF-8")
            statement_of_CF = pd.read_csv(self.stock_path + "\\" + "statement_of_CF" + str(key) + ".csv", encoding="UTF-8")
            self.fs_dict[key] = {'bs_sheet': bs_sheet, 'statement_of_CI': statement_of_CI, 'statement_of_CF': statement_of_CF}


        

if __name__ == "__main__":
    FIH = company("2707", "FIH")
    # FIH.read_fs_from_csv(3)
    # print(FIH.fs_dict[2018]['statement_of_CI'])
    # FIH.crawl_fs(2020)
    # FIH.crawl_fs(2019)
    # FIH.crawl_fs(2018)
    # FIH.write_fs_to_csv()

    LMT = company("2739", "LMT")
    # LMT.crawl_fs(2020)
    # LMT.crawl_fs(2019)
    # LMT.crawl_fs(2018)
    # LMT.write_fs_to_csv()

    PERIOD = 3
    progress = tqdm(total = PERIOD)
    for i in range(PERIOD):
        FIH.crawl_fs(YEAR-1-i)
        LMT.crawl_fs(YEAR-1-i)
        progress.update(1)
    FIH.write_fs_to_csv()
    LMT.write_fs_to_csv()