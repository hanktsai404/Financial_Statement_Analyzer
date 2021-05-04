'''
Financial Statement Analysis Main Program
Author: hanktsai404
Created at 03.05.2021
'''

import Company
import Analyzer
import time, datetime
import pandas as pd

YEAR = datetime.datetime.now().year

class program_manager():
    def __init__(self):
        self.company_list = []
        self.period = 1
        pass

    def crawl_financial_satement(self):
        while True:
            print("How many period?")
            s_period = input()
            self.period = int(s_period)
            print("Please enter index/name:")
            index_name = input()
            index = index_name.split("/")[0]
            name = index_name.split("/")[1]
            new_comp = Company.company(index, name)
            for i in range(self.period):
                new_comp.crawl_fs(YEAR-1-i)
            print("Do you want to save data?(y/n)")
            yn = input()
            if yn == "y":
                new_comp.write_fs_to_csv()
            self.company_list.append(new_comp)
            print("New company?(y/n)")
            yn = input()
            if yn == "n":
                break 

    def read_financial_satement(self):
        while True:
            print("How many period?")
            s_period = input()
            self.period = int(s_period)
            print("Please enter index/name:")
            index_name = input()
            index = index_name.split("/")[0]
            name = index_name.split("/")[1]
            new_comp = Company.company(index, name)
            new_comp.read_fs_from_csv(self.period)
            self.company_list.append(new_comp)
            print("New company?(y/n)")
            yn = input()
            if yn == "n":
                break
    
    def liquidity_analysis(self):
        analyzer = Analyzer.analyzer(self.company_list)
        analysis = analyzer.liquidity_analysis()
        print(analysis)
        print("Save data?(y/n)")
        yn = input()
        if yn == "y":
            target_csv = open("Liquidity_analysis.csv", "w", newline="", encoding = "UTF-8")
            analysis.to_csv(target_csv)
            target_csv.close()
    
    def leverages_analysis(self):
        analyzer = Analyzer.analyzer(self.company_list)
        analysis = analyzer.debt_converage_analysis()
        print(analysis)
        print("Save data?(y/n)")
        yn = input()
        if yn == "y":
            target_csv = open("Leverages_and_coverage_analysis.csv", "w", newline="", encoding = "UTF-8")
            analysis.to_csv(target_csv)
            target_csv.close()
    
    def dupont_analysis(self):
        analyzer = Analyzer.analyzer(self.company_list)
        analysis = analyzer.dupont_analysis()
        print(analysis)
        print("Save data?(y/n)")
        yn = input()
        if yn == "y":
            target_csv = open("Dupont_analysis.csv", "w", newline="", encoding = "UTF-8")
            analysis.to_csv(target_csv)
            target_csv.close()


    def start_program(self):
        while True:
            print("Please enter instruction:")
            print("0: Crawl financial statement, 1: Read financial statement, 2: Liquidity analysis\n3: Leverages and coverage analysis, 4: Dupont analysis, 5: Exit")
            instruction = input()
            if instruction == "0":
                self.crawl_financial_satement()
            elif instruction == "1":
                self.read_financial_satement()
            elif instruction == "2":
                self.liquidity_analysis()
            elif instruction == "3":
                self.leverages_analysis()
            elif instruction == "4":
                self.dupont_analysis()
            elif instruction == "5":
                break
            else:
                print("Input Error!")

manager = program_manager()
manager.start_program()
