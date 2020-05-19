import requests
import time
from bs4 import BeautifulSoup

overFlag = False
page = 1

# while True:
while page < 427:
    fout = open('CNRPage'+str(page)+'.txt', 'w', encoding='utf-8')
    targetUrl = 'http://was.cnr.cn/was5/web/search'
    header = {
        'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }
    param = {'page': str(page),
             'channelid': '234439',
             'searchword': '武汉 疫情',
             'keyword': '武汉 疫情',
             'orderby': 'RELEVANCE',
             'perpage':'10',
             'outlinepage': '10'}
    # if page > 1:
    #     param['start'] = 10 * (page - 1) + 1
    while True:
        req = requests.get(targetUrl, params=param, headers=header)
        # print(req.text)
        soup = BeautifulSoup(req.text, 'lxml')
        text = soup.find_all(
            'a', class_='searchresulttitle')
        if not (text is None):
            break
        time.sleep(6)
    # print(text)
    print(page)

    for each in text:
        try:
            link = each['href']
            print(link)
            title = each.string
            print(title)
            req = requests.get(url=link)
            req.encoding = 'gbk'
            # print(req.text)
            soup = BeautifulSoup(req.text, 'lxml')
            date = soup.find('div', class_='source').find('span')
            date = date.string
            print(date)
            year = int(date[:4])
            month = int(date[5:7])
            day = int(date[8:date.find(' ')])
            print(year, month, day)
            if (year < 2020) or (month < 1) or (month == 1 and day < 25):
                print("out of date")
                continue
            if (year < 2020) or (month > 3) or (month == 3 and day > 25):
                print("out of date")
                continue

            pars = soup.find('div', class_='TRS_Editor').find_all('p')
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
