#encoding=utf8
import BeautifulSoup
import HTMLParser
from selenium import webdriver

html_parser = HTMLParser.HTMLParser() #global parser
driver = webdriver.PhantomJS(executable_path='***/Downloads//phantomjs-2.1.1-windows//bin//phantomjs.exe')
driver.set_page_load_timeout(20)

def GetBlogHistory(url, direction):
    try:
        driver.get(url)
    except:
        print "Retry for timeout(20sec) exception, url: " + url
        GetBlogHistory(url, direction)
    content = driver.page_source
    soup = BeautifulSoup.BeautifulSOAP(content)
    if direction == 0 or direction == -1:
        llist = soup.find("div", attrs={"class": "pleft thide"})
        if(llist != None):
            lurl = dict(llist.contents[0].attrs)['href']
            print lurl + '  ' + html_parser.unescape(dict(llist.attrs)['a'])
            GetBlogHistory(lurl, -1)
    if direction == 0 or direction == 1:
        rlist = soup.find("div", attrs={"class": "pright thide"})
        if(rlist != None):
            rurl = dict(rlist.contents[0].attrs)['href']
            print rurl + '  ' + html_parser.unescape(dict(rlist.attrs)['a'])
            GetBlogHistory(rurl, 1)

url = 'http://micerin.blog.163.com/blog/static/30695072013723103422516/'  #seed page
GetBlogHistory(url, 0)
driver.close()
