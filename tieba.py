import requests
from lxml import etree
import  re
import os
"""
数据保存路径为：D:\\tiebatext\\tieba.txt
"""
class Tieba:
    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'}
        self.url = 'https://tieba.baidu.com/p/3138733512?see_lz=1&pn='
        self.enble = False

    # 总页数
    def getpage(self):
        url = self.url + str(1)
        html = requests.get(url=url, headers=self.headers).text
        s = etree.HTML(html)
        page = s.xpath('//li[@class="l_reply_num"]/span[2]/text()')[0]
        page = int(page)
        return page
    #urllist
    def geturllist(self,pages):
        items = []
        url = self.url + str(pages)
        html = requests.get(url = url, headers = self.headers).text
        s = etree.HTML(html)
        page = self.getpage()
        if pages != page:
            i = 1
            while i <= 29:
                content = s.xpath('//div[@class="d_post_content j_d_post_content "]')[i]
                content = content.xpath('string(.)').strip()
                items.append(content)
                i += 1
        elif pages == page:
            a = 1
            while a <= 21:
                content = s.xpath('//div[@class="d_post_content j_d_post_content "]')[a]
                content = content.xpath('string(.)').strip()
                items.append(content)
                a += 1
        return items
    #判断路径
    def path(self):
        if os.path.exists('D:\\tiebatext') == False:
            os.mkdir('D:\\tiebatext')
        if os.path.exists('D:\\tiebatext\\tieba.txt') == True:
            os.remove('D:\\tiebatext\\tieba.txt')
    #保存数据
    def savelist(self,items):
        f = open('D:\\tiebatext\\tieba.txt',"a",encoding='UTF-8')
        for item in items:
            f.write(item + '\n')
            f.write('\n')
        f.close()
    #运行
    def start(self):
        self.path()
        print('是否保存数据？1进行，0退出！')
        self.enble = True
        while self.enble:
            p = input()
            if p == '1':
                print('共%d页'% self.getpage())
                i = 1
                while i <= 5:
                    items =self.geturllist(i)
                    self.savelist(items)
                    print('正在保存第%d页内容'% i)
                    i += 1
                print('——程序结束——')
                self.enble = False
            elif p == '0':
                self.enble = False
            else:
                print('你的输入有误，请重新输入！')
                self.enble = True

spider = Tieba()
spider.start()
