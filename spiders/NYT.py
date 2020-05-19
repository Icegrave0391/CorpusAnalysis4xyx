import requests
import time
import json
from bs4 import BeautifulSoup

overFlag = False
page = 42

while True:
# while page < 3:
    fout = open('NTYPage'+str(page)+'.txt', 'w', encoding='utf-8')
    targetUrl = 'https://cn.nytimes.com/search/data/'
    header = {'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
          }
    param = {'query': '武汉 疫情',
             'lang': '',
             'dt': 'json',
             'from': str((page-1)*10),
             'size': '10'}
    while True:
        req = requests.get(targetUrl, params=param, headers=header)
        req.encoding = 'utf-8'
        text = json.loads(req.text)
        if not (text is None):
            print(text)
            break
        time.sleep(6)
    # print(text)
    print(page)

    for each in text['items']:
        try:
            # print(each)
            link = each['web_url_with_host']
            print(link)
            title = each['headline']
            print(title)
            date = each['publication_date']
            year = int(date[:4])
            pMonth = date.find('月')
            month = int(date[5:pMonth])
            day = int(date[pMonth+1:date.find('日')])
            print(year, month, day)
            if (year < 2020) or (month < 1) or (month == 1 and day < 25):
                print("[date out of range]1.25")
                continue
            if (year < 2020) or (month > 3) or (month == 3 and day > 25):
                print("[date out of range]3.25")
                continue

            req = requests.get(url=link)
            # print(req.text)
            soup = BeautifulSoup(req.text, 'lxml')
            pars = soup.find_all('div', class_='article-paragraph')
            # print(pars)

            fout.write(title)
            fout.write("\n")
            fout.write("\n".join([str(par) for par in pars]))
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
        time.sleep(2)

    if overFlag:
        break

    page = page + 1
