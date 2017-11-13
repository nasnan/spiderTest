from urllib import request
from bs4 import BeautifulSoup
import csv

url = 'https://movie.douban.com/top250'
head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}

req = request.Request(url = url,headers = head)
res = request.urlopen(req).read().decode('utf-8')

bsObj = BeautifulSoup(res,'lxml')


def store(name,content,rate):
    csvFile = open("test.csv","a+",newline = "")
    try:
        writer = csv.writer(csvFile)
        writer.writerow((name,content,rate))
    finally:
        csvFile.close()


def getNextUrl(startPage):
    global head
    req = request.Request(url = startPage, headers = head)
    html = request.urlopen(req).read().decode('utf-8')
    # html = request.urlopen(startPage)
    bsObj = BeautifulSoup(html,'lxml')
    nextUrl = bsObj.find("div",{"class":"article"}).find("span",{"class":"next"})
    if nextUrl.find("a") is not None:
        nextUrl = url+nextUrl.find("a").attrs['href']
    else:
        nextUrl = None
    return nextUrl


def getData(bsObj):
    article = bsObj.find("div",{"class":"article"})
    for item in article.findAll("div",{"class":"item"}):
        title = item.find("span",{"class":"title"}).get_text()
        rating = item.find("span",{"class":"rating_num"}).get_text()
        try:
            inq = item.find("span",{"class":"inq"}).get_text()
        except AttributeError as e:
            inq = '无短评'
        inq = inq.replace("'","\\\'")
        inq = inq.replace('"','\\\"')
        print(title,rating,inq)
        store(title,inq,rating)



def followOnePage(startPage):
    global url,head
    req = request.Request(url = url,headers = head)
    html = request.urlopen(req).read().decode('utf-8')
    # html = urlopen(startPage)
    bsObj = BeautifulSoup(html,'lxml')
    getData(bsObj)
    nextUrl = getNextUrl(startPage)
    if nextUrl is not None:
        followOnePage(nextUrl)

followOnePage(url)
