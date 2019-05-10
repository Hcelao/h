import os
import requests
import re
from lxml import etree

"""
数据保存地址为：D:\qsbktext1\qiushi.txt
"""

class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
        }
        self.enable = False

    #urllist
    def geturllist(self,pageIndex):
        pageUrl  = 'https://www.qiushibaike.com/hot/page/' + str(pageIndex)
        html = requests.get(url=pageUrl,headers=self.headers).text
        s = etree.HTML(html)
        urllist =  s.xpath('//div[@class="article block untagged mb15 typs_hot"]/a/@href')
        return urllist
    #数据
    def getItems(self,urllist):
        items = []
        for url in urllist:

            newurl = 'https://www.qiushibaike.com' + url
            item = []
            html = requests.get(url=newurl).text
            s = etree.HTML(html)
            #发表人
            name = s.xpath('//div[@class="side-user-top"]/span/text()')[0].replace("\n","")
            item.append(name)
            #内容
            content = s.xpath('//div[@class="content"]/text()')
            content = "".join(content)
            content = content.replace("\n","")
            item.append(content)
            #好笑数
            love = s.xpath('//span[@class="stats-vote"]/i[@class="number"]/text()')[0]
            item.append(love)

            items.append(item)
        return items

    #保存数据
    def saveItem(self,items):
        f = open('D:\\qsbktext1\\qiushi.txt',"a",encoding='UTF-8')

        for item in items:
            name = item[0]
            content = item[1]
            love = item[2]

            #写入文本
            f.write("发布人：" + name + '\n')
            f.write("内容：" + content + '\n')
            f.write("点赞数：" + love + '\n')
            f.write('\n\n')
        f.close()

    #判断路径
    def path(self):
        if os.path.exists('D:\\qsbktext1') == False:
            os.mkdir('D:\\qsbktext1')
        if os.path.exists('D:\\qsbktext1\\qiushi.txt') == True:
            os.remove('D:\\qsbktext1\\qiushi.txt')


     #运行
    def srart(self):
       self.path()
       print("正在读取糗事百科,按回车继续保存下一页，Q退出")
       self.enable = True
       while self.enable:
           urllist = self.geturllist(self.pageIndex)
           data = self.getItems(urllist)
           self.saveItem(data)
           print('已保存第%d页的内容' % self.pageIndex)
           p = input('是否继续保存：')
           if p != 'Q':
               self.pageIndex += 1
               self.enable = True
           else:
               print('程序结束！')
               self.enable = False

spider = QSBK()
spider.srart()