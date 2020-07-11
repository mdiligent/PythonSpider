import requests
from lxml import etree
import re
import json
import csv
import time
import random

# 获取网页源代码
def get_page(url):
    headers = {
        #如果需要登录可再加一个cookie键值对
        'USER-AGENT':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    response = requests.get(url=url,headers=headers)
    html = response.text
    return html

# 解析网页源代码，获取下一页链接
def parselink(html,base_url):
    link = None
    html_elem = etree.HTML(html)
    url = html_elem.xpath('//div[@id="paginator"]/a[@class="next"]/@href')
    if url:
        link = base_url + url[0]
    print(link)
    return link

# 解析网页源代码，获取数据
def parse4data(html):
    html = etree.HTML(html)
    agrees = html.xpath('//div[@class="comment-item"]/div[2]/h3/span[1]/span/text()')
    authods = html.xpath('//div[@class="comment-item"]/div[2]/h3/span[2]/a/text()')
    stars = html.xpath('//div[@class="comment-item"]/div[2]/h3/span[2]/span[2]/@title')
    contents = html.xpath('//div[@class="comment-item"]/div[2]/p/span/text()')
    data = zip(agrees,authods,stars,contents)
    return data

# 打开文件
def openfile(fm):
    fd = None
    if fm == 'txt':
        fd = open('douban_comment.txt','w',encoding='utf-8')
    elif fm == 'json':
        fd = open('douban_comment.json','w',encoding='utf-8')
    elif fm == 'csv':
        fd = open('douban_comment.csv','w',encoding='utf-8',newline='')
    return fd

# 将数据保存到文件
def save2file(fm,fd,data):
    if fm == 'txt':
        for item in data:
            fd.write('----------------------------------------\n')
            fd.write('agree：' + str(item[0]) + '\n')
            fd.write('authod：' + str(item[1]) + '\n')
            fd.write('star：' + str(item[2]) + '\n')
            fd.write('content：' + str(item[3]) + '\n')
    if fm == 'json':
        temp = ('agree','authod','star','content')
        for item in data:
            json.dump(dict(zip(temp,item)),fd,ensure_ascii=False)
    if fm == 'csv':
        writer = csv.writer(fd)
        for item in data:
            writer.writerow(item)

# 开始爬取网页
def crawl():
    moveID = input('请输入电影ID：')
    # while not re.match(r'\d{8}',moveID):
    #     moveID = input('输入错误，请重新输入电影ID：')
    base_url = 'https://movie.douban.com/subject/' + moveID + '/comments'
    fm = input('请输入文件保存格式（txt、json、csv）：')
    while fm!='txt' and fm!='json' and fm!='csv':
        fm = input('输入错误，请重新输入文件保存格式（txt、json、csv）：')
    fd = openfile(fm)
    print('开始爬取')
    link = base_url
    while link:
        print('正在爬取 ' + str(link) + ' ......')
        html = get_page(link)
        link = parselink(html,base_url)
        data = parse4data(html)
        save2file(fm,fd,data)
        time.sleep(random.random())
    fd.close()
    print('结束爬取')

if __name__ == '__main__':
    crawl()