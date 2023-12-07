# -*- coding: utf-8 -*-
import time
from datetime import datetime
import urllib.request
import requests
import pandas as pd
import csv
import sys
from bs4 import BeautifulSoup
import pandas as pd
import requests
from io import StringIO
import time
import json
import datetime
#import yfinance as yf
# test commit 2023 12.07
def transform_date(date):
        y, m, d = date.split('/')
        return str(int(y)+1911) + '/' + m  + '/' + d  #民國轉西元
def transform_data(data):
    data[0] = datetime.datetime.strptime(transform_date(data[0]), '%Y/%m/%d')
    data[1] = int(data[1].replace(',', ''))  #把千進位的逗點去除
    data[2] = int(data[2].replace(',', ''))
    data[3] = float(data[3].replace(',', ''))
    data[4] = float(data[4].replace(',', ''))
    data[5] = float(data[5].replace(',', ''))
    data[6] = float(data[6].replace(',', ''))
    data[7] = float(0.0 if data[7].replace(',', '') == 'X0.00' else data[7].replace(',', ''))  # +/-/X表示漲/跌/不比價
    data[8] = int(data[8].replace(',', ''))
    return data

def transform(data):
    return [transform_data(d) for d in data]
def get_stock_history(date, stock_no):
    quotes = []
    url = 'http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=%s&stockNo=%s' % ( date, stock_no)
    r = requests.get(url)
    data = r.json()
    return transform(data['data'])  #進行資料格式轉換
def create_df(date,stock_no):
    s = pd.DataFrame(get_stock_history(date, stock_no))
    s.columns = ['date', 'shares', 'amount', 'open', 'high', 'low', 'close', 'change', 'turnover']
                #"日期","成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數" 
    stock = []
    for i in range(len(s)):
        stock.append(stock_no)
    s['stockno'] = pd.Series(stock ,index=s.index)  #新增股票代碼欄，之後所有股票進入資料表才能知道是哪一張股票
    datelist = []
    for i in range(len(s)):
        datelist.append(s['date'][i])
    s.index = datelist  #索引值改成日期
    s2 = s.drop(['date'],axis = 1)  #刪除日期欄位
    mlist = []
    for item in s2.index:
        mlist.append(item.month)
    s2['month'] = mlist  #新增月份欄位
    return s2
def financial_statement(year, season, type='綜合損益彙總表',TYPEK='sli'):
#sii 上市 otc 上櫃
    if year >= 1000:
        year -= 1911
    
    if type == '綜合損益彙總表':
        url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb04'
    elif type == '資產負債彙總表':
        url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb05'
    elif type == '營益分析彙總表':
        url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb06'
    else:
        print('type does not match')
    #print(url)
    # 偽瀏覽器
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    payload = {
        'encodeURIComponent':1,
        'step':1,
        'firstin':1,
        'off':1,
        'TYPEK':str(TYPEK),
        'year':str(year),
        'season':str(season),
    }
    #r = requests.post(url, data=json.dumps(payload), headers=headers)
    r = requests.post(url, {
        'encodeURIComponent':1,
        'step':1,
        'firstin':1,
        'off':1,
        'TYPEK':str(TYPEK),
        'year':str(year),
        'season':str(season),
    })
   

    r.encoding = 'utf8'
    dfs = pd.read_html(r.text, header=None)
    #(pd.DataFrame(dfs)).to_csv('sii.csv',encoding='utf_8_sig')
    #dfs = pd.read_csv(r.text)
    #print(dfs) 
    if type == '營益分析彙總表':
        dataset = pd.concat(dfs[:], axis=0, sort=False)
        dataset.columns = ['公司代號','公司名稱','營業收入(百萬元)','毛利率(%)(營業毛利)/(營業收入)','營業利益率(%)(營業利益)/(營業收入)','稅前純益率(%)(稅前純益)/(營業收入)','稅後純益率(%)(稅後純益)/(營業收入)']
        dataset.set_index(['公司代號'])
        #del dataset['Unnamed: 0']
        dataset = dataset.drop_duplicates(subset=None, keep='first', inplace=False)
        dataset = dataset[1:]
        #dataset.to_csv('營益分析彙總表'+str(TYPEK)+'.csv',encoding='utf_8_sig')
        return dataset
    elif type == '綜合損益彙總表':
        dataset = pd.concat(dfs[:], axis=0, sort=False)
        #(pd.DataFrame(dataset)).to_csv('test.csv',encoding='utf_8_sig')
        #dataset.columns =['0','保險負債準備淨變動','停業單位損益','公司代號','公司名稱','其他收益及費損淨額','其他綜合損益（淨額）','利息以外淨收益','利息淨收益','原始認列生物資產及農產品之利益（損失）','合併前非屬共同控制股權損益','合併前非屬共同控制股權綜合損益淨額','呆帳費用、承諾及保證責任準備提存','基本每股盈餘（元）','已實現銷貨（損）益','所得稅費用（利益）','所得稅（費用）利益','支出及費用','收益','未實現銷貨（損）益','本期其他綜合損益（稅後淨額）','本期淨利（淨損）','本期稅後淨利（淨損）','本期綜合損益總額','淨利（損）歸屬於母公司業主','淨利（損）歸屬於非控制權益','淨利（淨損）歸屬於共同控制下前手權益','淨利（淨損）歸屬於母公司業主','淨利（淨損）歸屬於非控制權益','淨收益','營業利益','營業利益（損失）','營業外損益','營業外收入及支出','營業成本','營業收入','營業毛利（毛損）','營業毛利（毛損）淨額','營業費用','生物資產當期公允價值減出售成本之變動利益（損失）','稅前淨利（淨損）','綜合損益總額歸屬於共同控制下前手權益','綜合損益總額歸屬於母公司業主','綜合損益總額歸屬於非控制權益','繼續營業單位本期淨利（淨損）','繼續營業單位稅前損益']
        #dataset.columns =['公司代號','公司名稱','利息淨收益','利息以外淨損益','呆帳費用、承諾及保證責任準備提存','營業費用','繼續營業單位稅前淨利（淨損）','所得稅費用（利益）','繼續營業單位本期稅後淨利（淨損）','停業單位損益','合併前非屬共同控制股權損益','本期稅後淨利（淨損）','其他綜合損益（稅後）','合併前非屬共同控制股權綜合損益淨額','本期綜合損益總額（稅後）','淨利（損）歸屬於母公司業主','淨利（損）歸屬於共同控制下前手權益','淨利（損）歸屬於非控制權益','綜合損益總額歸屬於母公司業主','綜合損益總額歸屬於共同控制下前手權益','綜合損益總額歸屬於非控制權益','基本每股盈餘（元）','收益','支出及費用','營業利益','營業外損益','稅前淨利（淨損）','繼續營業單位本期淨利（淨損）','本期淨利（淨損）','本期其他綜合損益（稅後淨額）','本期綜合損益總額','淨利（淨損）歸屬於共同控制下前手權益','營業收入','營業成本','原始認列生物資產及農產品之利益（損失）','生物資產當期公允價值減出售成本之變動利益（損失）','營業毛利（毛損）','未實現銷貨（損）益','已實現銷貨（損）益','營業毛利（毛損）淨額','其他收益及費損淨額','營業利益（損失）','營業外收入及支出','其他綜合損益（淨額）','淨利（淨損）歸屬於母公司業主','淨利（淨損）歸屬於非控制權益','利息以外淨收益','淨收益','保險負債準備淨變動','繼續營業單位稅前損益','所得稅（費用）利益','繼續營業單位稅前純益（純損）','繼續營業單位本期純益（純損）','其他綜合損益（稅後淨額）','收入','支出','其他綜合損益']
        dataset.set_index(['公司代號'])
        dataset = dataset.drop_duplicates(subset=None, keep='first', inplace=False)
        dataset = dataset[:]
       
        #print(dataset)
        return dataset
    else:
        return pd.concat(dfs[1:], axis=0, sort=False)\
                 .set_index(['公司代號'])\
                 .apply(lambda s: pd.to_numeric(s, errors='ceorce'))
               
             #.apply(lambda s: pd.to_numeric(s, errors='ceorce'))
    #             .set_index(['公司代號'])\         
    #return pd.concat(dfs[1:], axis=0, sort=False)\
    #         .set_index(['公司代號'])\
    #         .apply(lambda s: pd.to_numeric(s, errors='ceorce'))
    """
    elif type == '綜合損益彙總表':
        dataset = pd.concat(dfs[:], axis=0, sort=False)
        dataset.columns =['公司代號','公司名稱','利息淨收益','利息以外淨損益','呆帳費用、承諾及保證責任準備提存','營業費用','繼續營業單位稅前淨利（淨損）','所得稅費用（利益）','繼續營業單位本期稅後淨利（淨損）','停業單位損益','合併前非屬共同控制股權損益','本期稅後淨利（淨損）','其他綜合損益（稅後）','合併前非屬共同控制股權綜合損益淨額','本期綜合損益總額（稅後）','淨利（損）歸屬於母公司業主','淨利（損）歸屬於共同控制下前手權益','淨利（損）歸屬於非控制權益','綜合損益總額歸屬於母公司業主','綜合損益總額歸屬於共同控制下前手權益','綜合損益總額歸屬於非控制權益','基本每股盈餘（元）','收益','支出及費用','營業利益','營業外損益','稅前淨利（淨損）','繼續營業單位本期淨利（淨損）','本期淨利（淨損）','本期其他綜合損益（稅後淨額）','本期綜合損益總額','淨利（淨損）歸屬於共同控制下前手權益','營業收入','營業成本','原始認列生物資產及農產品之利益（損失）','生物資產當期公允價值減出售成本之變動利益（損失）','營業毛利（毛損）','未實現銷貨（損）益','已實現銷貨（損）益','營業毛利（毛損）淨額','其他收益及費損淨額','營業利益（損失）','營業外收入及支出','其他綜合損益（淨額）','淨利（淨損）歸屬於母公司業主','淨利（淨損）歸屬於非控制權益','利息以外淨收益','淨收益','保險負債準備淨變動','繼續營業單位稅前損益','所得稅（費用）利益','繼續營業單位稅前純益（純損）','繼續營業單位本期純益（純損）','其他綜合損益（稅後淨額）','收入','支出','其他綜合損益']
        dataset.set_index(['公司代號'])
        #del dataset['Unnamed: 0']
        dataset = dataset.drop_duplicates(subset=None, keep='first', inplace=False)
        dataset = dataset[1:]
        return dataset
    """
def monthly_report(year, month,type='sii'): #殖利率(%) 本益比 股價淨值比    
    # 假如是西元，轉成民國
    if year > 1990:
        year -= 1911
    
    url = 'https://mops.twse.com.tw/nas/t21/'+str(type)+'/t21sc03_'+str(year)+'_'+str(month)+'_0.html'
    if year <= 98:
        url = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'.html'
    print('get_url:'+url)
    # 偽瀏覽器
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    # 下載該年月的網站，並用pandas轉換成 dataframe
    r = requests.get(url, headers=headers)
    #print(r)
    r.encoding = 'cp950'
    dfs = pd.read_html(StringIO(r.text), encoding='cp950')
    #print(dfs)
 
    df = pd.concat([df for df in dfs if df.shape[1] <= 11 and df.shape[1] > 5])
    if 'levels' in dir(df.columns):
        df.columns = df.columns.get_level_values(1)
    else:
        df = df[list(range(0,10))]
        column_index = df.index[(df[0] == '公司代號')][0]
        df.columns = df.iloc[column_index]
    
    df['當月營收'] = pd.to_numeric(df['當月營收'], 'coerce')
    df = df[~df['當月營收'].isnull()]
    df = df[df['公司代號'] != '合計']
    return df

    return df
def download(): #個股日本益比、殖利率及股價淨值比
    CSV_URL = 'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&selectType=ALL'
    #CSV_URL = 'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=csv&date=20200514&selectType=ALL'

    # 偽瀏覽器
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # 下載該年月的網站，並用pandas轉換成 dataframe
    r = requests.get(CSV_URL, headers=headers)
    r.encoding = 'cp950'
    dfs = pd.read_csv(CSV_URL, encoding='cp950',  skiprows=1)
    dfs.to_csv('個股日本益比.csv',encoding='utf_8_sig')
    #print(dfs[dfs['證券代號'] == '2330'])
 
def get_allseason_profit_report():
    now = datetime.datetime.now()
    data ={}
    n_days =4*2 #4*2
    year = now.year -1
    season = int(now.month/4) 
    if season == 0:
        season = 4
        year -= 1
    while len(data) <n_days:
        mydate = "GET_season_report"+str(year) +  "Q"+str(season) + ".csv"
        print(mydate)
        print(len(data))
        #print(len(data))
        try:
            data['%dQ%d'%(year, season)] =  pd.merge(financial_statement(year,season, type='營益分析彙總表',TYPEK='sii'),(financial_statement(year,season, type='營益分析彙總表',TYPEK='otc')),  how="outer")
           # data = data.drop_duplicates(subset=None, keep='first', inplace=False)
        except Exception as e:
            print('get 404, please check if the revenues are not revealed')
        season -= 1
        if season == 0:
            season = 4
            year -= 1
        time.sleep(2)
    for k in data.keys():
        data[k].index = data[k]['公司代號']

    df2 = pd.DataFrame({k:df['營業利益率(%)(營業利益)/(營業收入)'] for k, df in data.items()}).transpose()
    df2.to_csv('營業利益率(%).csv',encoding='utf_8_sig')

    df3 = pd.DataFrame({k:df['稅前純益率(%)(稅前純益)/(營業收入)'] for k, df in data.items()}).transpose()
    df3.to_csv('稅前純益率(%).csv',encoding='utf_8_sig')

    df4 = pd.DataFrame({k:df['稅後純益率(%)(稅後純益)/(營業收入)'] for k, df in data.items()}).transpose()
    df4.to_csv('稅後純益率(%).csv',encoding='utf_8_sig')

    df1 = pd.DataFrame({k:df['毛利率(%)(營業毛利)/(營業收入)'] for k, df in data.items()}).transpose()
    #df.index = pd.to_datetime(df.index)
    df1.to_csv('毛利率(%).csv',encoding='utf_8_sig')
    df1 = df1.sort_index()


    return df1
def get_allseason_EPS_report():
    now = datetime.datetime.now()
    data ={}
    n_days =2
    year = now.year # 轉成民國
    season = int(now.month/4)
    while len(data) <n_days:
        mydate = "GET_season_EPSreport"+str(year) + "Q"+ str(season) + ".csv"
        print(mydate)
        print(len(data))
        #print(len(data))
        try:
            rec1 = (financial_statement(year,season, type='綜合損益彙總表',TYPEK='ski'))
            rec2 = (financial_statement(year,season, type='綜合損益彙總表',TYPEK='otc'))

            for k in rec1.keys():
                rec1[k] = rec1[k].astype(object)
            for k in rec2.keys():
                rec2[k] = rec2[k].astype(object)
            data['%dQ%d'%(year, season)] = pd.merge(rec1,rec2,how="outer")

            
            print('got it2')

        except Exception as e:
            print(e)
            print('get 404, please check if the revenues are not revealed')
        season -= 1
        if season == 0:
            season = 4
            year -= 1
        time.sleep(2)


    for k in data.keys():
        data[k].index = data[k]['公司代號']
    

    tmp=[]
    for k in data.keys():
        t1 = pd.DataFrame(data[k]['基本每股盈餘（元）'])
        t1 = t1.dropna()
        for z in t1.count() :
            print(t1[z]['基本每股盈餘（元）'])

        print(t1)
        tmp[k] = t1 

    df4 = pd.DataFrame({k:df['基本每股盈餘（元）'] for k, df in data.items()}).transpose()
    df4.to_csv('基本每股盈餘.csv',encoding='utf_8_sig')

def get_oneyear_monthly_report():
    now = datetime.datetime.now()
    data ={}
    n_days = 12 #12*10
    year = now.year
    month = now.month
    while len(data) <n_days:
        mydate = "GET_monthly_report"+str(year) +  str(month) + ".csv"
        print(mydate)
        print(len(data))
        try:
            data['%d-%d-01'%(year, month)] = monthly_report(year, month,type='sii').append( monthly_report(year, month,type='otc'))
            
            #print(data)
        except Exception as e:
            print('get 404, please check if the revenues are not revealed')
        month -= 1
        if month == 0:
            month = 12
            year -= 1
       
        time.sleep(10)
    for k in data.keys():
        data[k].index = data[k]['公司代號']
 
    df1 = pd.DataFrame({k:df['當月營收'] for k, df in data.items()}).transpose()
    df1.index = pd.to_datetime(df1.index)
    df1.to_csv('月營收.csv',encoding='utf_8_sig')
    df1 = df1.sort_index()

    df2 = pd.DataFrame({k:df['去年同月增減(%)'] for k, df in data.items()}).transpose()
    df2.index = pd.to_datetime(df2.index)
    df2 = df2.sort_index()
    df2.to_csv('YOY.csv',encoding='utf_8_sig')

    df3 = pd.DataFrame({k:df['前期比較增減(%)'] for k, df in data.items()}).transpose()
    df3.index = pd.to_datetime(df3.index)
    df3 = df3.sort_index()
    df3.to_csv('QoQ.csv',encoding='utf_8_sig')

    df1.to_csv("月營收.csv",encoding='utf_8_sig')
    return df1


#download()  #個股日本益比、殖利率及股價淨值比

get_oneyear_monthly_report()
get_allseason_profit_report()
#get_allseason_EPS_report()






