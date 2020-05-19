import time
import json
import requests
from requests.cookies import RequestsCookieJar
from bs4 import BeautifulSoup
from selenium import webdriver

# fout = open('test.txt', 'w')

browser = webdriver.Chrome('chromedriver.exe')
# browser.delete_all_cookies()
browser.get('https://www.wsj.com/')
time.sleep(10)
'''
cookiesList = [str(each) for each in browser.get_cookies()]
# fout.write("old cookies\n")
# fout.writelines(cookiesList)
# fout.write("\n")

browser.get('https://sso.accounts.dowjones.com/login?state=g6Fo2SAtY2RpNTlsNnl1LVROSGpMN1d6WkpXOEdIM0dzMW5HbKN0aWTZIGxWbFFvblJuaXlyTUtGVkUtUnh6OGhHNGQ1QkdSVjN3o2NpZNkgNWhzc0VBZE15MG1KVElDbkpOdkM5VFhFdzNWYTdqZk8&client=5hssEAdMy0mJTICnJNvC9TXEw3Va7jfO&protocol=oauth2&scope=openid%20idp_id%20roles%20email%20given_name%20family_name%20djid%20djUsername%20djStatus%20trackid%20tags%20prts&response_type=code&redirect_uri=https%3A%2F%2Faccounts.wsj.com%2Fauth%2Fsso%2Flogin&nonce=eac1c495-a299-4898-8b7a-f604c6008026&ui_locales=en-us-x-wsj-83-2&ns=prod%2Faccounts-wsj&savelogin=on#!/signin')
time.sleep(3)
elem = browser.find_element_by_name('username')
elem.send_keys('procedure2012@hotmail.com')
elem = browser.find_element_by_name('password')
elem.send_keys('xyr:262514!')
# elem.find_element_by_('//button')
# print(elem.text)
# elem.click()
time.sleep(10)
newCookies = browser.get_cookies()
json.dump(newCookies, fout)
'''
fin = open("test.txt","r")
logInfo = json.load(fin)
# print(logInfo)
for each in logInfo:
    if 'expiry' in each:
        del each['expiry']
    browser.add_cookie(each)

overFlag = False
page = 1
s = requests.session()
s.verify = False
s.headers = {'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
            }
# while True:
while page < 36:
    fout = open('WSJPage'+str(page)+'.txt', 'w', encoding='utf-8')
    targetUrl = 'https://cn.wsj.com/zh-hans/search'
    param = {'id': '{"params":{"count":"20","daysback":"90d","language":"zhcn","sort":"date-desc","exclude_products":"Deloitte Blogs","time-zone":"Asia/Hong_Kong","query":"中国 疫情","union":"AND","min-date":"2020/01/23","max-date":"2020/03/24","page":"'+str(page)+'"},"clientId":"grandcanyon","database":"wsjschinese"}',
             'type': 'dnsa_search_full'}
    while True:
        req = s.get(targetUrl, params=param)
        req.encoding = 'utf-8'
        # print(req.text)
        text = json.loads(req.text)
        if not (text is None):
            print(len(text['collection']), text['collection'])
            break
        time.sleep(6)
    print(page)
    for each in text['collection']:
        try:
            id = each['id']
            articaleType = each['type']
            param = {'id': id, 'type': articaleType}
            req = s.get(targetUrl, params=param)
            # print(req.text)
            soup = json.loads(req.text)
            title = soup['data']['headline']
            link = soup['data']['url']
            year = int(id[7:11])
            month = int(id[11:13])
            day = int(id[13:15])
            print(title)
            print(link)
            print(year, month, day)
            browser.get(link)
            time.sleep(2)
            pars = browser.find_element_by_class_name('article-content')
            # print(pars.text)
            fout.write(title)
            fout.write("\n")
            fout.write(pars.text)
            fout.write("\n*\n")
        except IndexError:
            print("IndexError")
            time.sleep(2)
            continue
        except AttributeError:
            print("AttributeError")
            time.sleep(2)
            continue
        except TypeError:
            print("TypeError")
            time.sleep(2)
            continue
        # time.sleep(2)
    if overFlag:
        break
    page = page + 1
