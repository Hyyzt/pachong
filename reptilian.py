import urllib.request
import urllib.response
from pachong import data
from bs4 import BeautifulSoup

tagUrl = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-hot#%E6%96%87%E5%AD%A6'


##获取html
def getWebHtml(web):
    response = urllib.request.urlopen(web)
    html = response.read()
    result = html.decode('utf-8')
    return result


##将网页的html解析成一个list集合
def parseDataHtml(html, Tag):
    dataList = []
    soup = BeautifulSoup(html)
    data_star = ''
    data_pl = ''
    data_author = ''
    data_name = ''
    tag = Tag
    for link in soup.find_all('li', {'class': 'subject-item'}):
        if link is None:
            return
        for a in link.find_all('a'):
            if a.has_attr('title'):
                data_name = a.get('title')
        for div in link.find_all('div'):
            if 'pub' in div.get('class'):
                data_author = div.get_text().strip()
            if 'star' in div.get('class'):
                for span in div.find_all('span'):
                    if 'rating_nums' in span.get('class'):
                        data_star = span.get_text()
                    if 'pl' in span.get('class'):
                        data_pl = span.get_text().strip()
        dataList.append(data.data(data_name, data_author, data_star, data_pl, tag))
    print("本次爬到的数据size:%d" % dataList.__len__())
    return dataList


def parseTagHtml(html):
    bigTag = ''
    smallTag = ''
    soup = BeautifulSoup(html)
    for div in soup.find_all('div'):
        if div.get('class') is None:
            for a in div.find_all('a', {'name': "文学"}):
                print(a)


# parseTagHtml(getWebHtml(tagUrl))

# 获取不同页码的地址
def getUrl(page):
    URL = "https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=" + str(page) + "&type=T"
    return URL


page = 0

result = []

while (True):
    dataList = parseDataHtml(
        getWebHtml(getUrl(page)),
        '小说')
    if dataList.__len__() is 0:
        break
    else:
        page += 20
        result.extend(dataList)
        print("第 %d 已经跑完了" % page)

print(result.__len__())
for da in result:
    print("name : " + da.name + " , author : " + da.author + ", star : " + da.star
          + ", pl : ", da.pl + ", tag = ", da.tag)
