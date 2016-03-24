#encoding=utf8
import BeautifulSoup
import HTMLParser
import time
from selenium import webdriver

html_parser = HTMLParser.HTMLParser() #global parser
service_args = [
    '--proxy=[proxy ip:port]',#localhost:8080',
    '--proxy-type=socks5',#socks5',
    ]
driver = webdriver.PhantomJS(executable_path='***//phantomjs-2.1.1-windows//bin//phantomjs.exe', service_args=service_args)
driver.set_page_load_timeout(20) #set pageload timeout for phantomjs

printtimeoutexcept = 1 #control whether display timeout retry log
printblognum = 1 #control whether print blog number in iteration loop
totalnum = 0
currentnum = 0

def GetBlogHistory(url, direction):
    global totalnum
    global currentnum

    if currentnum > 15:
        print "sleep 30 seconds before continuing retrieving new instances"
        time.sleep(30) #sleep 30seconds after retrieved 20 instances, way to avoid block from site for too frequent access...
        currentnum = 0
    currentnum +=1

    try:
        driver.get(url)
    except:
        if printtimeoutexcept == 1:
            print "retry for timeout(20sec) exception, url: " + url
        GetBlogHistory(url, direction)
    content = driver.page_source
    soup = BeautifulSoup.BeautifulSOAP(content)
    if direction == 0 or direction == -1:
        llist = soup.find("div", attrs={"class": "pleft thide"})
        if(llist != None):
            lurl = dict(llist.contents[0].attrs)['href']
            if printblognum == 1:
                totalnum +=1
                print "%d. %s %s"%(totalnum, lurl, html_parser.unescape(dict(llist.attrs)['a']))
            else:
                print lurl + '  ' + html_parser.unescape(dict(llist.attrs)['a'])
            GetBlogHistory(lurl, -1)
    if direction == 0 or direction == 1:
        rlist = soup.find("div", attrs={"class": "pright thide"})
        if(rlist != None):
            rurl = dict(rlist.contents[0].attrs)['href']
            if printblognum == 1:
                totalnum +=1
                print "%d. %s %s"%(totalnum, rurl, html_parser.unescape(dict(rlist.attrs)['a']))
            else:
                print rurl + '  ' + html_parser.unescape(dict(rlist.attrs)['a'])
            GetBlogHistory(rurl, 1)

url = 'http://cskun1989.blog.163.com/blog/static/12767822420162124374543/' #seed page
GetBlogHistory(url, 0)
driver.close()
