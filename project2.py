 # Project Option 2. Equity Research of S&P 500 Stocks
# User Interface:
# 1. The user can choose a company from a list of stocks in S&P 500 index
# Based on the choice of the company:
# 2. Your code calculates the short-term cost of capital (weighted-average of book debt and market equity)
#    Cost of equity uses the risk-free rate (3%), market return (10%) and the company's BETA
#    Cost of debt uses the ratio of interest expense and total debt (both long-term and short-term debts)
#    Weighs in WACC is based on the total book value of debt and total market equity (market cap)
# 3. You code calculates the short-term growth rate which is the higher number of two growth rates: Revenue growth rate and Earnings growth rate in the past four years
#    If both numbers are negative, then use 3% instead
# 4. Long-term cost of capital is the average of the short-term cost of capital of all firms in the same industry
# 5. Long-term growth rate is the average of the short-term growth rate of all firms in the same industry
# 6. Your code calculates the equity value per share using a two-stage model with a 10-year high growth period and a terminal value for low-growth period
# 7. If the equity value calculated is below market price, your code also suggests an alternative stock in the same industry of your choice, but it has a higher valuation relative to the market stock price


import random as rd
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import tkinter as tk
import matplotlib.figure as fig
import matplotlib.backends.backend_tkagg as bac
import csv
from tkinter import *
import random
import time

big_break = random.randint(10,25)
small_break = random.randint(5,10)

def DownloadData(ticker, begin_day, end_day):
    try:
        dt.datetime.strptime(begin_day, '%Y-%m-%d')
        dt.datetime.strptime(end_day, '%Y-%m-%d')
        mydata = yf.download(ticker, begin_day, end_day)
        return mydata['Adj Close']
    except:
        print('Date must be entered as YYYY-MM-DD')



##############################################################




#functions for buttons
def ExitNow():
    mywindow.destroy()
    return







########################################################

#company valuation

########################################################


#cost of capital calculation

rf = 0.03
rm = 0.10
taxrate = 0.21


def cost_of_capital(ticker):
    fin_data =  yf.Ticker(ticker)

    #cost of Equity
    beta = fin_data.get_info('beta')
    time.sleep(small_break)
    so = fin_data.get_info()['sharesOutstanding']
    coe = rf + (rm - rf)*beta
        #costofdebt
    Int_exp = fin_data.get_balancesheet()['Interest Expense']
    time.sleep(small_break)
    total_debt = fin_data.get_balancesheet()['Total Debt']
    time.sleep(small_break)
    total_equity = fin_data.get_balancesheet()['Total Equity']
    time.sleep(small_break)
    total_assets = fin_data.get_balancesheet()['Total Assets']
    w_e = total_equity / total_assets
    r_e = 0.03 + (r_f-0.10)*beta_company
    w_d = 1- w_e
    r_d = int_exp / total_debt
    coc = w_d * r_d + w_e * r_e
    return coc

########################################################




#low growth rate calculation

# 3. You code calculates the short-term growth rate which is the higher number of two growth rates: Revenue growth rate and Earnings growth rate in the past four years
#    If both numbers are negative, then use 3% instead


def shortterm_calculation(ticker):

    fin_data =  yf.Ticker(ticker)
    #revenue growth rate

    revenues = fin_data.get_financials()['Revenues']
    reversed_revenues = revenues.iloc[0:4:-1]
    revenue_growth = (reversed_revenues - reversed_revenues.shift(1))/reversed_revenues
    low_g_rev = mean(revenue_growth)
    #earning growth rate
    time.sleep(small_break)
    earnings = fin_data.get_financials()['Earnings']
    reversed_earnings = earnings.iloc[0:4:-1]
    earnings_growth = (reversed_earnings - reversed_earnings.shift(1))/reversed_revenues
    low_g_earning = mean(earnings_growth)
    if low_g_rev > 0  and low_g_earning> 0:
        if low_g_rev > low_g_earning :
            short_term_rate = low_g_rev
        else:
            short_term_rate = low_g_earning
    else:
            short_term_rate = 0.03

    #print("internet down!")

    return short_term_rate

########################################################


#high growthrate calculation

# Load all U.S. stocks in all sectors:
stock_list = pd.read_csv('sp500.csv')
tickers = stock_list['Ticker']
industries = stock_list['Industry']
founded = stock_list['Founded']

#industry list(that is sorted alphabetically without duplicates)
industry_set = set(industries.to_list())
industry_sorted = sorted(list(industry_set))

#making a Industry finding dataframe
ticker_index_df =pd.concat([tickers,industries], axis=1)
ticker_index_df= ticker_index_df.set_index('Ticker')
ticker_index_df_tr = ticker_index_df.transpose() #this one
# command for finding industry of ticker:   ticker_index_df_tr.loc['Industry','A'])

#Making a df with Industries as Index
industries_df = pd.concat([tickers,industries], axis=1)
industries_df = industries_df.set_index('Industry')
industries_df = industries_df.sort_values(by =['Industry'])

#making above df into a dictionary
gb = industries_df.groupby(['Industry'])
result = gb['Ticker'].unique()
result.coloumns = ['Tickers']
result.name = "Ticker list"
result_dict = result.to_dict() #this one
# commoand for finding all tickers in the industry: result_dict.get("Energy")

def longetermgcalc(ticker):
    ind_name = ticker_index_df_tr.loc['Industry',ticker]
    for each_ticker in ind_name:
        stc_tick = shortterm_calculation(each_ticker)
        numerator_sum += stc_tick
        nof_tickers += 1
    long_term_rate = numerator / numberoffirms
    return long_term_rate

def longetermcoccalc(ticker):
    ind_name = ticker_index_df_tr.loc['Industry',ticker]
    for each_ticker in ind_name:
        stc_tick = cost_of_capital(each_ticker)
        numerator_sum += stcoc_tick
        nof_tickers += 1
    long_terc_coc = numerator / numberoffirms
    return long_term_coc

########################################################

# Valuation calculation

def val(ticker):

    fin_data = yf.Ticker(ticker)

    shares = fin_data.get_info()['sharesOutstanding'][0]
    time.sleep(small_break)
    cash = fin_data.get_info()['totalCash'][0]
    time.sleep(big_break)
    debt = fin_data.get_info()['totalDebt'][0]
    time.sleep(small_break)
    opt_cf = fin_data.get_info()['operatingCashflow'][0]
    time.sleep(big_break)
    int_exp = fin_data.get_financials()['Interest Expense'][0]
    tax_shield = - int_exp * tax_rate
    time.sleep(small_break)
    cap_ex = fin_data.get_cashflow()['Capital Expenditures'][0]

    my_index = ['Period','Opt CF','Int Exp','Tax Shield','CapEx','CF','TV','FCF'] #building the index for the df

    my_data = np.array([0, opt_cf, int_exp, tax_shield, cap_ex, 0, 0, 0]) #building the first row
    my_series = pd.Series(my_data,name=current_year,index=my_index)  #creating a series with index and first year info
    #but why is there no
    my_df = pd.DataFrame(my_series)

    # High growth period
    for year in range(2021,2026):
        my_data = my_data *(1+ high_g)
        my_series = pd.Series(my_data, name = year, index = my_index)
        my_series.loc['Period'] = year - 2020
        my_df = pd.concat([my_df,my_series], axis  =1)

    # Low growth period

    my_data = my_data *(1+ low_g)
    my_series = pd.Series(my_data,name =2026,index = my_index)
    my_series.loc['Period'] = 6
    my_df = pd.concat([my_df,my_series], axis = 1)





    #needs editing

    my_df.loc['CF'] = my_df.loc[['Opt CF','Int Exp','Tax Shield','CapEx']].sum()
    my_df.loc['TV',2025] = my_df.loc['CF', 2026] / [ low_cc- low_g]
    my_df.loc['FCF'] = my_df.loc['CF'] + my_df.loc['TV']
    my_df = my_df.drop(columns = [2020,2026])
    my_df.loc['PV'] = my_df.loc['FCF'] / (1+high_cc) ** my_df.loc['Period']
    #print(my_df)

    # Calculate equity value per share
    equity = (my_df.loc['PV'].sum() - debt + cash) /shares
    return equity

########################################################

#interfacefunctions and data

mywindow = tk.Tk()


#General outline

mywindow.geometry('1000x700')
mywindow.title('My Equity Research Valaution App')

#create list box
myframe = tk.Frame(mywindow)
myframe.place(x=30, y=70)
myscroll = tk.Scrollbar(myframe, orient=tk.VERTICAL)



tk.Label(mywindow, text = 'Step 1: Select a stock from the list below!').place(x=30, y=50)
tk.Label(mywindow, text = 'Step 2: This is the stock you have selected').place(x=30, y=350)
tk.Label(mywindow, text = 'Step 3: See the recommendation for the stock you picked below').place(x=500, y=50)
tk.Label(mywindow, text = 'Step 4: Alternate investment option down below ( if your selection is overvalued )').place(x=500, y=350)

tk.Label(mywindow, bg=('red'),fg=('white'), text = 'PLEASE GIVE THE PROGRAM 10-20 MINUTES TO PROCESS YOUR REQUEST!', font = ('Bold',15)).place(x=50, y=650) #RED COLOUR
tk.Button(mywindow,text="Exit",command = ExitNow).place(x= 900, y=600)








reccomendationlabel = Label(mywindow, text="")
reccomendationlabel.place(x=500, y=70)
Alternatereccomlabel = Label(mywindow, text="")
Alternatereccomlabel.place(x=500, y=370)


def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    try:
        todays_data = ticker.history(period='1d')
    except:
        print("Internet Down!")
    return todays_data['Close'][0]

file1 = open('C:/Users/advai/Desktop/Fall 2021/DA/FINAL PROJECT/sp500.csv')
reader1 = csv.reader(file1)
data1 = list(reader1)
del(data1[0])

list_of_entries = []
for x in list(range(0,len(data1))):
    list_of_entries.append(data1[x][0])
var1 = StringVar(value = list_of_entries)


myselect = tk.Listbox(myframe,listvariable = var1,width = 70, height = 12, yscrollcommand=myscroll.set)
#main function metafunction

def update():

    index = myselect.curselection()[0]
    companylabel2.config(text = data1[index][1])
    tickerlabel2.config(text = data1[index][0])
    industrylabel2.config(text = data1[index][2])
    headquarterslabel2.config(text = data1[index][3])
    ticker = data1[index][0]
    low_cc = cost_of_capital(ticker)
    low_g = shortterm_calculation(ticker)
    high_cc = longetermcoccalc(ticker)
    high_g = longtermgcalc(ticker)
    value_of_equity = val(ticker)

    fin_data = yf.Ticker(ticker)
    shares = fin_data.get_info()['sharesOutstanding'][0]

    price_per_share = value_of_equity / shares
    market_price = get_current_price(ticker)

    if price_per_share > market_price:
        print('##################','\n', 'The reccomendation is:', '\n', 'Buy stock. The stock is undervalued as the value of share of the selected ticker:', price_per_share, ' is greater than the market price:', market_price,'\n','#########################')
        ###label.config here
        reccomendationlabel.config(text = 'Buy stock. The stock is undervalued as the value of share of the company is greater than the market price.[ check the window for complete answers]')
    else:
        #print('The reccomendation is:', '\n', 'Dont buy. Overvalued. Buy instead the following company:','\n')
        reccomendationlabel.config(text = 'Dont buy. Overvalued. Buy instead the following company. Check window for results. [look under step 4]')
        respectiveindustry = ticker_index_df_tr.loc['Industry',ticker]
        #find respetive industry from df
        respectiveindustrylist = result_dict.get(respectiveindustry)
        #respectiveindustrylist = array of all industries from respective industry

        for eachcompany in respectiveindustrylist:

            #checkif variables need to be changed
                low_cc = cost_of_capital(eachcompany)
                low_g = shortterm_calculation(eachcompany)
                high_cc = longetermcoccalc(eachcompany)
                high_g = longtermgcalc(eachcompany)
                value_of_equity = val(eachcompany)

                fin_data = yf.ticker(eachcompany)
                shares = fin_data.get_info()['sharesOutstanding'][0]

                price_per_share = value_of_equity / shares
                market_price = get_current_price(eachcompany)

                if price_per_share > market_price:
                    print('##################','\n', 'The reccomendation is:','\n', eachcompany, '\n', 'Buy stock. The stock is undervalued as the value of share of the selected ticker:', price_per_share, ' is greater than the market price:', market_price,'\n','#########################')
                    #add to a dicitonary with Ticker name, pricepershare, marketprice,difference between pricepershare and marketprice
                    #return ticker value with greatest difference between price per share and market price
                    # that is the reccomendation
                    #alternatereccomlabel.config
                    alternatereccomlabel.config(text = 'Buy stock. The stock is undervalued as the value of share of the company is greater than the market price.[ check the window for complete answers]')


                    #find the stock with the highest difference between the two
                    #that is the stock reccomendation
                    ###label.config here
                else:
                    print('##################','\n', 'The reccomendation is:','\n', eachocompany,"is Overvalued",'##################')
                    #print('The stock you selected is in an industry with all stocks being overvalued. so buy the following stock from the same industry: ')
                    #alternatereccomlabel.config(text = 'Dont buy. Overvalued. Buy instead the following company.[look under step 4]')
                    ###label.config here
                    # the stock with the highest differnece between pricepershare and marketprice is the reccomendation

    return None
#### interface again
myselect.pack(side=tk.LEFT)
myscroll.config(command=myselect.yview)
myscroll.pack(side=tk.RIGHT, fill=tk.Y)

tk.Button(mywindow,text="Update Selection and Value!", command= update).place(x= 200, y=300)
companylabel = Label(mywindow, text="Company:").place(x=30, y=370)
tickerlabel = Label(mywindow, text="Symbol:").place(x=30, y=390)
industrylabel = Label(mywindow, text="Industry:").place(x=30, y=410)
headquarterslabel = Label(mywindow, text="Headquarters:").place(x=30, y=430)

companylabel2 = Label(mywindow, text="")
companylabel2.place(x=200, y=370)
tickerlabel2 = Label(mywindow, text="")
tickerlabel2.place(x=200, y=390)
industrylabel2 = Label(mywindow, text="")
industrylabel2.place(x=200, y=410)
headquarterslabel2 = Label(mywindow, text="")
headquarterslabel2.place(x=200, y=430)

reccomendationlabel = Label(mywindow, text="")
reccomendationlabel.place(x=500, y=70)
Alternatereccomlabel = Label(mywindow, text="")
Alternatereccomlabel.place(x=500, y=370)




# Meta function

#
#
#def valsystem():
#    # data1[index][0]
#    #find currentselection
#    index1 = myselect.curselection()[0]
#    ticker = data1[index1][0]
#    low_cc = cost_of_capital(ticker)
#    low_g = shortterm_calculation(ticker)
#    high_cc = longetermcoccalc(ticker)
#    high_g = longtermgcalc(ticker)
#    value_of_equity = val(ticker)
#
#    fin_data = yf.Ticker(ticker)
#    shares = fin_data.get_info()['sharesOutstanding'][0]
#
#    price_per_share = value_of_equity / shares
#    market_price = get_current_price(ticker)
#
#    if price_per_share > market_price:
#        print('##################','\n', 'The reccomendation is:', '\n', 'Buy stock. The stock is undervalued as the value of share of the selected ticker:', price_per_share, ' is greater than the market price:', market_price,'\n','#########################')
#        ###label.config here
#        reccomendationlabel.config(text = 'Buy stock. The stock is undervalued as the value of share of the company is greater than the market price.[ check the window for complete answers]')
#    else:
#        #print('The reccomendation is:', '\n', 'Dont buy. Overvalued. Buy instead the following company:','\n')
#        reccomendationlabel.config(text = 'Dont buy. Overvalued. Buy instead the following company. Check window for results. [look under step 4]')
#        respectiveindustry = ticker_index_df_tr.loc['Industry',ticker]
#        #find respetive industry from df
#        respectiveindustrylist = result_dict.get(respectiveindustry)
#        #respectiveindustrylist = array of all industries from respective industry
#
#        for eachcompany in respectiveindustrylist:
#
#            #checkif variables need to be changed
#                low_cc = cost_of_capital(eachcompany)
#                low_g = shortterm_calculation(eachcompany)
#                high_cc = longetermcoccalc(eachcompany)
#                high_g = longtermgcalc(eachcompany)
#                value_of_equity = val(eachcompany)
#
#                fin_data = yf.ticker(eachcompany)
#                shares = fin_data.get_info()['sharesOutstanding'][0]
#
#                price_per_share = value_of_equity / shares
#                market_price = get_current_price(eachcompany)
#
#                if price_per_share > market_price:
#                    print('##################','\n', 'The reccomendation is:','\n', eachcompany, '\n', 'Buy stock. The stock is undervalued as the value of share of the selected ticker:', price_per_share, ' is greater than the market price:', market_price,'\n','#########################')
#                    #add to a dicitonary with Ticker name, pricepershare, marketprice,difference between pricepershare and marketprice
#                    #return ticker value with greatest difference between price per share and market price
#                    # that is the reccomendation
#                    #alternatereccomlabel.config
#                    alternatereccomlabel.config(text = 'Buy stock. The stock is undervalued as the value of share of the company is greater than the market price.[ check the window for complete answers]')
#
#
#                    #find the stock with the highest difference between the two
#                    #that is the stock reccomendation
#                    ###label.config here
#                else:
#                    print('##################','\n', 'The reccomendation is:','\n', eachocompany,"is Overvalued",'##################')
#                    #print('The stock you selected is in an industry with all stocks being overvalued. so buy the following stock from the same industry: ')
#                    #alternatereccomlabel.config(text = 'Dont buy. Overvalued. Buy instead the following company.[look under step 4]')
#                    ###label.config here
#                    # the stock with the highest differnece between pricepershare and marketprice is the reccomendation


########################################################

###############User interface###############################

########################################################









########################################################
########################################################
########################################################
########################################################
