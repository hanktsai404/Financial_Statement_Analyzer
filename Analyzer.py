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
    str_num = str_num.replace(",","")
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
    
    def debt_converage_analysis(self):
        col_names = ["Ratio"]
        le_ratios = ["Liability_to_equity_ratio"]
        dc_ratios = ["Debt_to_capital_ratio"]
        Int_conv_ebs = ["Interest_coverage(earnings_based)"]
        Int_conv_cbs = ["Interest_coverage(cash_flow_based)"]
        for comp in self.companies:
            for key in comp.fs_dict.keys():
                col_names.append(comp.name + str(key))
                BS = comp.fs_dict[key]['bs_sheet']
                CI = comp.fs_dict[key]['statement_of_CI']
                CF = comp.fs_dict[key]['statement_of_CF']

                tl_row = BS.loc[BS["Title"] == "負債總計 Total liabilities",:]
                tl = acct_num_str_to_float(tl_row.iloc[0][str(key)])
                te_row = BS.loc[BS["Title"] == "權益總額 Total equity",:]
                if te_row.empty:
                    te_row = BS.loc[BS["Title"] == "權益總計 Total equity",:]
                te = acct_num_str_to_float(te_row.iloc[0][str(key)])
                le_ratio = round(tl/te, 2)
                le_ratios.append(le_ratio)

                dc_ratio = round(tl/(tl+te), 2)
                dc_ratios.append(dc_ratio)

                ni_pretax_row = CI.loc[CI["Title"] == "繼續營業單位稅前淨利（淨損）Profit (loss) from continuing operations before tax",:]
                ni_pretax = acct_num_str_to_float(ni_pretax_row.iloc[0][str(key)])
                interest_exp_row = CF.loc[CF["Title"] == "利息費用 Interest expense",:]
                interest_exp = acct_num_str_to_float(interest_exp_row.iloc[0]["In"+str(key)])
                tax_exp_row = CI.loc[CI["Title"] == "所得稅費用（利益）合計　Total tax expense (income)",:]
                tax_exp = acct_num_str_to_float(tax_exp_row.iloc[0][str(key)])
                Int_conv_eb = round((ni_pretax+interest_exp+tax_exp)/interest_exp, 2)
                Int_conv_ebs.append(Int_conv_eb)

                cf_op_row = CF.loc[CF["Title"] == "營業活動之淨現金流入（流出）Net cash flows from (used in) operating activities",:]
                cf_op = acct_num_str_to_float(cf_op_row.iloc[0]["In"+str(key)])
                tax_paid_row = CF.loc[CF["Title"] == "退還（支付）之所得稅　Income taxes refund (paid)"]
                tax_paid = -acct_num_str_to_float(tax_paid_row.iloc[0]["In"+str(key)])
                Int_conv_cb = round((cf_op+interest_exp+tax_paid)/interest_exp, 2)
                Int_conv_cbs.append(Int_conv_cb)

        ratios = [le_ratios, dc_ratios, Int_conv_ebs, Int_conv_cbs]
        return pd.DataFrame(ratios, columns = col_names)

    def dupont_analysis(self):
        col_names = ["Ratio"]
        op_profit_margins = ["Operating_profit_margin"]
        op_asset_tos = ["X Operating_asset_turnover"]
        ro_op_assets = ["= Return_on_operating_assets"]
        op_to_buss = ["X Operation assets/Business assets"]
        ro_inv_assets = ["+ Return_on_non-operating_investments"]
        inv_to_buss = ["X Non-operating_investments/Business assets"]
        robas = ["= ROBA"]
        effect_interest_rate_aftaxs = ["- Effective_interest_after_tax"]
        spreads = ["= Spread"]
        leverages = ["X Financial_leverage"]
        robas_1 = ["+ ROBA"]
        roes = ["= ROE"]
        for comp in self.companies:
            for key in comp.fs_dict.keys():
                col_names.append(comp.name + str(key))
                BS = comp.fs_dict[key]['bs_sheet']
                CI = comp.fs_dict[key]['statement_of_CI']
                CF = comp.fs_dict[key]['statement_of_CF']

                ni_pretax_row = CI.loc[CI["Title"] == "繼續營業單位稅前淨利（淨損）Profit (loss) from continuing operations before tax",:]
                ni_pretax = acct_num_str_to_float(ni_pretax_row.iloc[0][str(key)])
                ni_row = CI.loc[CI["Title"] == "本期淨利（淨損）Profit (loss)",:]
                ni = acct_num_str_to_float(ni_row.iloc[0][str(key)])
                tax_rate = round((1-(ni/ni_pretax)), 2)

                interest_exp_row = CF.loc[CF["Title"] == "利息費用 Interest expense",:]
                interest_exp = acct_num_str_to_float(interest_exp_row.iloc[0]["In"+str(key)])
                interest_exp_afttax = interest_exp*(1 - tax_rate)

                nipat_row = CI.loc[CI["Title"] == "營業外收入及支出合計　Total non-operating income and expenses",:]
                nipat = (acct_num_str_to_float(nipat_row.iloc[0][str(key)]) + interest_exp)*(1 - tax_rate)
                nopat = ni - nipat + interest_exp_afttax

                tl_row = BS.loc[BS["Title"] == "負債總計 Total liabilities",:]
                tl = acct_num_str_to_float(tl_row.iloc[0][str(key)])
                te_row = BS.loc[BS["Title"] == "權益總額 Total equity",:]
                if te_row.empty:
                    te_row = BS.loc[BS["Title"] == "權益總計 Total equity",:]
                te = acct_num_str_to_float(te_row.iloc[0][str(key)])
                ta = te + tl

                finasset_row = BS.loc[BS["Title"] == "透過損益按公允價值衡量之金融資產－流動 Current financial assets at fair value through profit or loss",:]
                if not finasset_row.empty:
                    finasset = acct_num_str_to_float(finasset_row.iloc[0][str(key)])
                finasset_row = BS.loc[BS["Title"] == "按攤銷後成本衡量之金融資產－流動 Current financial assets at amortised cost",:]
                if not finasset_row.empty:
                    finasset =  finasset + acct_num_str_to_float(finasset_row.iloc[0][str(key)])
                finasset_row = BS.loc[BS["Title"] == "透過其他綜合損益按公允價值衡量之金融資產－非流動 Non-current financial assets at fair value through other comprehensive income",:]
                if not finasset_row.empty:
                    finasset =  finasset + acct_num_str_to_float(finasset_row.iloc[0][str(key)])
                finasset_row = BS.loc[BS["Title"] == "按攤銷後成本衡量之金融資產－非流動 Non-current financial assets at amortised cost",:]
                if not finasset_row.empty:
                    finasset =  finasset + acct_num_str_to_float(finasset_row.iloc[0][str(key)])
                finasset_row = BS.loc[BS["Title"] == "採用權益法之投資 Investments accounted for using equity method",:]
                if not finasset_row.empty:
                    finasset =  finasset + acct_num_str_to_float(finasset_row.iloc[0][str(key)])
                deferred_tax_row = BS.loc[BS["Title"] == "遞延所得稅資產 Deferred tax assets",:]
                deferred_tax = 0
                if not deferred_tax_row.empty:
                    deferred_tax = acct_num_str_to_float(deferred_tax_row.iloc[0][str(key)])
                op_asset = ta - finasset - deferred_tax
                inv_asset = finasset
                bus_asset = op_asset + inv_asset

                rev_row = CI.loc[CI["Title"] == "營業收入合計　Total operating revenue",:]
                rev = acct_num_str_to_float(rev_row.iloc[0][str(key)])

                op_profit_margin = round(nopat/rev, 2)
                op_profit_margins.append(op_profit_margin)
                op_asset_to = round(rev/op_asset, 2)
                op_asset_tos.append(op_asset_to)
                ro_op_asset = round(nopat/op_asset, 2)
                ro_op_assets.append(ro_op_asset)
                ro_inv_asset = round(nipat/inv_asset, 2)
                ro_inv_assets.append(ro_inv_asset)
                op_to_bus = round(op_asset/bus_asset, 2)
                op_to_buss.append(op_to_bus)
                inv_to_bus = 1 - op_to_bus
                inv_to_buss.append(inv_to_bus)
                roba = round((ro_op_asset*op_to_bus) + (ro_inv_asset*inv_to_bus), 2)
                robas.append(roba)
                robas_1.append(roba)
                effect_interest_rate_aftax = round(interest_exp_afttax/tl, 2)
                effect_interest_rate_aftaxs.append(effect_interest_rate_aftax)
                spread = roba - effect_interest_rate_aftax
                spreads.append(spread)
                leverage = round(tl/te, 2)
                leverages.append(leverage)
                roe = round(roba + (spread*leverage), 2)
                roes.append(roe)
                
        ratios = [op_profit_margins, op_asset_tos, ro_op_assets, op_to_buss, ro_inv_assets, inv_to_buss, robas, effect_interest_rate_aftaxs, spreads, leverages, robas_1, roes]
        return pd.DataFrame(ratios, columns = col_names)



if __name__ == "__main__":
    FIH = company("2707", "FIH")
    FIH.crawl_fs(2020)
    FIH.crawl_fs(2019)
    LMT = company("2739", "LMT")
    LMT.crawl_fs(2020)
    LMT.crawl_fs(2019)
    analyzer = analyzer([FIH, LMT])
    print(analyzer.dupont_analysis())