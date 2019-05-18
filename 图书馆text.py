import os
from  lxml import etree
import  requests
import re
class LIB():
    def keydate(self,word):
        date = {"searchPath": "全部","keyword":"1","dbName": "all"}
        date["keyword"] = word
        return date

    def pagedate(self,word,num):
        date = date = {"searchPath": "全部","keyword":"1","dbName": "all"}
        date["keyword"] = word
        date["pageNow"] = str(num)
        return date

    def posturl(self):
        url =  'http://ilib.gcu.edu.cn/WebOPAC/search_searchResultView'

        p = input('请输入你的检索信息：')
        date = self.keydate(p)
        respone = requests.post(url=url,data=date).text
        html = etree.HTML(respone)
        page = html.xpath('//ol[@class="fr"]/li/a/@onclick')[-1]
        page = int(re.findall(r"\d+", page)[0])
        result = html.xpath('//div[@class="operation"]/h4/b/text()')[0]
        print('搜到的结果有：'+result)

        nameitem = []
        urllists = []
        i = 1
        while i <= page:
            date1 = self.pagedate(p,i)
            url = 'http://ilib.gcu.edu.cn/WebOPAC/search_searchResultView'
            date = date1
            respone = requests.post(url=url, data=date).text
            html = etree.HTML(respone)
            bookname = html.xpath('//div[@class="textFL fl"]/h4/a/text()')
            nameitem.extend(bookname)
            urllist = html.xpath('//div[@class="BookDetails"]/input/@value')
            urllists.extend(urllist)
            i += 1
        contents = []
        for i in urllists:
            content = []
            url = 'http://ilib.gcu.edu.cn/WebOPAC/searchDetail_detailView?primaryId=' + i + '&referLocation='
            respone = requests.get(url).text
            html = etree.HTML(respone)
            name =  html.xpath('//div[@class="FLMessageText fl"]/ul/li/b/text()')
            worker = html.xpath('//div[@class="FLMessageText fl"]/ul/li[2]/text()')
            chubanse =  html.xpath('//div[@class="FLMessageText fl"]/ul/li[3]/text()')
            content.append(name)
            content.append(worker)
            content.append(chubanse)
            n1 = html.xpath('//table[@class="table"]/tbody/tr/td[2]/text()')
            n2 = html.xpath('//table[@class="table"]/tbody/tr/td[3]/text()')
            n3 = html.xpath('//table[@class="table"]/tbody/tr/td[4]/text()')
            n4 = html.xpath('//table[@class="table"]/tbody/tr/td[5]/text()')
            content.append(n1)
            content.append(n2)
            content.append(n3)
            content.append(n4)
            contents.append(content)
        for i in contents:
            print('书名:' + i[0][0])
            print(i[1][0])
            print(i[2][0])
            print('索书号：'+"  ".join(i[3]))
            print('条码号：' + "  ".join(i[4]))
            print('馆藏地：' + "  ".join(i[5]))
            print('文献状态：' + "  ".join(i[6]))
            print()

s = LIB()
s.posturl()
