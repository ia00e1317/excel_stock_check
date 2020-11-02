import pandas as pd
#import openpyxl
import openpyxl as opx
from datetime import date

""""""
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import urllib
import time

def checkKeywords(url,check_list,site):

    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

    flg = True
    for check in check_list:
        classname = check[0]
        tagtype = check[1]
        attribute = check[2]
        keyword = check[3]

        txt_list = []
        for target in soup.find_all(class_=classname):#
            for element in target.find_all(tagtype):#
                if attribute:
                    #txt_list.append(element.get(attribute).strip())
                    txt_list.append(element.get(attribute))
                else:
                    #txt_list.append(element.text.strip())
                    txt_list.append(element.text)

        if keyword in txt_list:
            pass
        else:
            flg = False

    if flg:
        return "〇"
    else:
        return "×"
""""""


filename = "stock_check.xlsx"
exl=pd.ExcelWriter(filename, engine='openpyxl')
exl.book=opx.load_workbook(filename)
exl.sheets=dict((ws.title, ws) for ws in exl.book.worksheets)

df_in = pd.read_excel(filename, sheet_name="settings")
df_in = df_in.fillna(False)

out_list = []
lines = df_in.values
for i,line in enumerate(lines):
    code = line[0]
    site = line[1]
    name = line[2]
    url = line[3]
    classname_1 = line[4]
    tagtype_1 = line[5]
    attribute_1 = line[6]
    keyword_1 = line[7]
    classname_2 = line[8]
    tagtype_2 = line[9]
    attribute_2 = line[10]
    keyword_2 = line[11]

    check_list = [ [ classname_1,tagtype_1,attribute_1,keyword_1 ] ]
    if classname_2 and tagtype_2:
        check_list.append( [ classname_2,tagtype_2,attribute_2,keyword_2 ] )
    result = checkKeywords(url,check_list,site)
    add = [result,code,site,name,url]
    out_list.append(add)
    print(add)

df_out = pd.DataFrame()
df_out = pd.DataFrame({"結果":[], "コード":[], "サイト":[], "商品名":[], "URL":[] })
for i,outline in enumerate(out_list):
    df_out.loc[i] = outline

sheetname = "result_" + str(date.today())
df_out.to_excel(exl, sheet_name=sheetname, index=False)
exl.save()
print( "[" + filename + "]:[" + sheetname + "]" )

