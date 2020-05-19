import requests
import time
from bs4 import BeautifulSoup

overFlag = False
page = 1

# while True:
while page < 25:
    fout = open('BBCPage'+str(page)+'.txt', 'w', encoding='utf-8')
    targetUrl = 'https://www.bbc.com/zhongwen/simp/search'
    header = {'referer': 'https://www.bbc.com/zhongwen/simp/51222586',
          'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
          }
    param = {'q': '武汉 疫情'}
    if page > 1:
        param['start'] = 10 * (page - 1) + 1
    while True:
        req = requests.get(targetUrl, params=param, headers=header)
        # print(req.text)
        soup = BeautifulSoup(req.text, 'lxml')
        text = soup.find_all('div', class_='hard-news-unit hard-news-unit--regular faux-block-link')
        if not (text is None):
            break
        time.sleep(6)
    # print(text)
    print(page)

    for each in text:
        try:
            # print(each)
            link = each.a['href']
            print(link)
            title = each.a.string
            print(title)
            req = requests.get(url=link)
            # print(req.text)
            soup = BeautifulSoup(req.text, 'lxml')
            date = soup.find('div', class_='date date--v2').string
            year = int(date[:4])
            month = int(date[5:date.find('月')])
            day = int(date[9:date.find('日')])
            if (year < 2020) or (month < 1) or (month == 1 and day < 25):
                print("out of date")
                continue
            if (year < 2020) or (month > 3) or (month == 3 and day > 25):
                print("out of date")
                continue
            pars = soup.find('div', class_='story-body__inner').find_all('p').encode('gb2312')
            print(pars)

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
