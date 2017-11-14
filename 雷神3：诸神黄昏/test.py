from urllib import request
from bs4 import BeautifulSoup
import requests
import csv


head = {'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
raw_cookies = 'bid=V3sXsf3h2aM; ll="118172"; ct=y; ps=y; _ga=GA1.2.1110410350.1509450230; _gid=GA1.2.269881452.1510647917; gr_user_id=fd90710c-08d5-4284-9d72-f5b2e3da940b; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1510660373%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _vwo_uuid_v2=8B8F44D6CC749FE8167175340E35F54C|7f9074441c49eaf5231f94f8dd37659d; __utma=30149280.1110410350.1509450230.1510644685.1510658005.9; __utmc=30149280; __utmz=30149280.1510658005.9.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; __utmv=30149280.5548; __utma=81379588.1110410350.1509450230.1510660372.1510660372.1; __utmc=81379588; __utmz=81379588.1510660372.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; push_noty_num=0; push_doumail_num=0; ap=1; _pk_id.100001.3ac3=0ffd3fd7fee583c3.1510660373.1.1510661763.1510660373.; ue="876987944@qq.com"; dbcl2="55483954:Q5TNrjJ6ksg"'

cookies = {}
for line in raw_cookies.split(";"):
    key,value = line.split('=',1)
    cookies[key] = value

firstUrl = 'https://movie.douban.com/subject/25821634/comments?start=0&limit=20&sort=new_score&status=P&percent_type='
req = requests.get(firstUrl,cookies = cookies,headers = head)
html = req.text
bsObj = BeautifulSoup(html, 'lxml')

def getData(bsObj):
    article = bsObj.find("div", {"class": "article"})
    for commen in article.findAll("div", {"class": "comment-item"}):
        info = commen.find("span", {"class": "comment-info"})
        name = info.find("a").get_text()
        isRead = info.find("span").get_text()
        title = info.findAll("span")[1].attrs['title']
        star = info.findAll("span")[1].attrs['class'][0][7:8]
        vote = commen.find("span", {"class": "comment-vote"}).find("span", {"class": "votes"}).get_text()
        time = info.find("span", {"class": "comment-time"}).attrs['title']
        comment = commen.find("p").get_text()

        store(name, isRead, title, star, vote, time, comment)

def store(name, isread, title, star, vote, time, comment):
    csvFile = open("Tttttr.csv", 'a+', newline = '')
    try:
        writer = csv.writer(csvFile)
        writer.writerow((name, isread, title, star, vote, time, comment))
    except UnicodeEncodeError as e:
        pass
    finally:
        csvFile.close()


        # try:
        #     comment = commen.find("p").get_text()
        # except AttributeError as e:
        #     comment = ''

# print(bsObj)
getData(bsObj)