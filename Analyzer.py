'''
Financial Statement Analysis: Analyzer
Author: hanktsai404
Created at 03.05.2021
'''

from Company import company
import matplotlib.pyplot as plotter
import pandas as pd
import numpy as np
import time, datetime

YEAR = datetime.datetime.now().year

def acct_num_str_to_float(str_num):
    if "(" in str_num:
        float_num = -(float(str_num[1:-1]))
    else:
        float_num = float(str_num)
    return float_num

class analyzer():
    def __init__(self, companies: list):
        self.companies = companies
        self.NCOMP = len(companies)
    
    def liquidity_analysis(self):
        col_names = ["Ratio"]
        current_ratios = ["Current_ratio"]
        quick_ratios = ["Quick_ratio"]
        cash_ratios = ["Cash_ratio"]
        op_cf_ratios = ["Operating_cash_ratio"]
        for comp in self.companies:
            for key in comp.fs_dict.keys():
                col_names.append(comp.name + str(key))
                BS = comp.fs_dict[key]['bs_sheet']
                CF = comp.fs_dict[key]['statement_of_CF']

                current_asset_row = BS.loc[BS["Title"] == "流動資產合計 Total current assets",:]
                current_asset = acct_num_str_to_float(current_asset_row.iloc[0][str(key)])
                current_liability_row = BS.loc[BS["Title"] == "流動負債合計 Total current liabilities",:]
                current_liability = acct_num_str_to_float(current_liability_row.iloc[0][str(key)])
                current_ratio = round(current_asset/current_liability, 2)
                current_ratios.append(current_ratio)

                inventory_row = BS.loc[BS["Title"] == "存貨 Current inventories",:]
                inventory = acct_num_str_to_float(inventory_row.iloc[0][str(key)])
                prepaid_exp_row = BS.loc[BS["Title"] == "預付款項 Prepayments",:]
                prepaid_exp = acct_num_str_to_float(prepaid_exp_row.iloc[0][str(key)])
                quick_ratio = round((current_asset-inventory-prepaid_exp)/current_liability, 2)
                quick_ratios.append(quick_ratio)

                cash_row = BS.loc[BS["Title"] == "現金及約當現金 Cash and cash equivalents",:]
                cash = acct_num_str_to_float(cash_row.iloc[0][str(key)])
                fvtpl_row = BS.loc[BS["Title"] == "透過損益按公允價值衡量之金融資產－流動 Current financial assets at fair value through profit or loss",:]
                fvtpl = acct_num_str_to_float(fvtpl_row.iloc[0][str(key)])
                cash_ratio = round((cash+fvtpl)/current_liability, 2)
                cash_ratios.append(cash_ratio)

                cf_op_row = CF.loc[CF["Title"] == "營業活動之淨現金流入（流出）Net cash flows from (used in) operating activities",:]
                cf_op = acct_num_str_to_float(cf_op_row.iloc[0]["In"+str(key)])
                op_cf_ratio = round(cf_op/current_liability, 2)
                op_cf_ratios.append(op_cf_ratio)

        ratios = [current_ratios, quick_ratios, cash_ratios, op_cf_ratios]
        return pd.DataFrame(ratios, columns = col_names)








if __name__ == "__main__":
    FIH = company("2707", "FIH")
    FIH.crawl_fs(2020)
    FIH.crawl_fs(2019)
    LMT = company("2739", "LMT")
    LMT.crawl_fs(2020)
    LMT.crawl_fs(2019)
    analyzer = analyzer([FIH,LMT])
    print(analyzer.liquidity_analysis())