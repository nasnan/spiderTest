
'''
豆瓣电影Top250
名字 评分 短评
'''


from urllib.request import urlopen
from bs4 import BeautifulSoup

url = 'https://movie.douban.com/top250'

def getNextUrl(startPage):
    global url
    html = urlopen(startPage)
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
        print(title,rating,inq)

def followOnePage(startPage):
    html = urlopen(startPage)
    bsObj = BeautifulSoup(html)
    getData(bsObj)
    nextUrl = getNextUrl(startPage)
    if nextUrl is not None:
        followOnePage(nextUrl)

followOnePage(url)