from flask import Flask
import os
from lxml import etree
import requests
import re
import json
"""
书名参数在url传入
"""
app = Flask(__name__)
@app.route('/')
def kk():
    return "请在url上输入书名搜索"

def keydate(word):
    date = {"searchPath": "全部", "keyword": "1", "dbName": "all"}
    date["keyword"] = word
    return date
def pagedate(word,num):
     date = date = {"searchPath": "全部","keyword":"1","dbName": "all"}
     date["keyword"] = word
     date["pageNow"] = str(num)
     return date


@app.route('/<bookname>')
def index(bookname):
    url = 'http://ilib.gcu.edu.cn/WebOPAC/search_searchResultView'
    date = keydate(bookname)
    respone = requests.post(url=url, data=date).text
    html = etree.HTML(respone)
    page = html.xpath('//ol[@class="fr"]/li/a/@onclick')[-1]
    page = int(re.findall(r"\d+", page)[0])

    urllists = []
    i = 1
    while i <= page:
        date1 = pagedate(bookname, i)
        url = 'http://ilib.gcu.edu.cn/WebOPAC/search_searchResultView'
        date = date1
        respone = requests.post(url=url, data=date).text
        html = etree.HTML(respone)
        urllist = html.xpath('//div[@class="BookDetails"]/input/@value')
        urllists.extend(urllist)
        i += 1
    contents = {}
    a = 1
    for i in urllists:
        b = {}
        url = 'http://ilib.gcu.edu.cn/WebOPAC/searchDetail_detailView?primaryId=' + i + '&referLocation='
        respone = requests.get(url).text
        html = etree.HTML(respone)
        name = html.xpath('//div[@class="FLMessageText fl"]/ul/li/b/text()')
        worker = html.xpath('//div[@class="FLMessageText fl"]/ul/li[2]/text()')
        chubanse = html.xpath('//div[@class="FLMessageText fl"]/ul/li[3]/text()')
        n1 = html.xpath('//table[@class="table"]/tbody/tr/td[2]/text()')
        n2 = html.xpath('//table[@class="table"]/tbody/tr/td[3]/text()')
        n3 = html.xpath('//table[@class="table"]/tbody/tr/td[4]/text()')
        n4 = html.xpath('//table[@class="table"]/tbody/tr/td[5]/text()')
        b["书名"] = name[0]
        b["worker"] = worker[0]
        b["path"] = chubanse[0]
        b["索书号"] = "  ".join(n1)
        b["条码号"] = "  ".join(n2)
        b["馆藏地"] = "  ".join(n3)
        b["文献状态"] = "  ".join(n4)
        contents[a] = b
        a += 1
    return json.dumps(contents, indent=2)

if __name__ == '__main__':
    app.run()
