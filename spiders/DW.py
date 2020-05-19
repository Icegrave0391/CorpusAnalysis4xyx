import requests
import time
from bs4 import BeautifulSoup

#177
overFlag = False
page = 2

while page < 51:
# while True:
    fout = open('DWPage'+str(page)+'.txt', 'w', encoding='utf-8')
    targetUrl = 'https://www.dw.com/search/'
    header = {'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
          }
    param = {'languageCode': 'zh',
            'item': '武汉 疫情',
            'searchNavigationId': '9058',
            'from': '25.01.2020',
            'to': '25.03.2020',
            'sort': 'DATE',
            'resultsCounter': 498}
    while True:
        req = requests.get(targetUrl, params=param, headers=header)
        # print(req.text)
        soup = BeautifulSoup(req.text, 'lxml')
        textDiv = soup.find_all('div', class_='searchResult')
        # print(textDiv)
        if not (textDiv is None):
            # print(textDiv)
            break
        time.sleep(10)
    print(page)

    for each in textDiv:
        try:
            link = each.a['href']
            # title = each.find('h2').string
            date = each.find('span', class_='date').string
            req = requests.get("https://www.dw.com"+link)
            soup = BeautifulSoup(req.text, 'lxml')
            title = soup.find('div', class_='col3').h1.string
            print(title)
            # print(link)
            day = date[:2]
            month = date[3:5]
            year = date[6:]
            print(year, month, day)
            pars = soup.find('div', class_='longText').find_all('p')
            fout.write(title)
            fout.write("\n")
            fout.write("\n".join([str(par) for par in pars]))
            fout.write("\n*\n")
        except IndexError:
            print("IndexError")
            continue
        except AttributeError:
            print("AttributeError")
            continue
        except TypeError:
            print("TypeError")
            continue
        time.sleep(2)
    if overFlag:
        break
    # time.sleep(4)
    page = page + 1
