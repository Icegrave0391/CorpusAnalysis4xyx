#coding:utf-8
import re
import jieba

stopWordsFile = open("stopwords.txt", "r", encoding='utf-8')
stopWords = [word[:-1] for word in stopWordsFile.readlines()]
jieba.add_word("新冠肺炎")
jieba.add_word("冠性肺炎")
jieba.add_word("新型冠性肺炎")
jieba.add_word("新型冠状病毒")
jieba.add_word("火神山")
jieba.add_word("雷神山")
jieba.add_word("方舱医院")
jieba.add_word("人民日报")
jieba.add_word("人民网")
jieba.add_word("卫星通讯社")
jieba.add_word("谭德塞")
jieba.add_word("新华网")
jieba.add_word("新华社")
jieba.add_word("武汉肺炎")
jieba.add_word("中国病毒")
jieba.add_word("武汉病毒")
jieba.add_word("中国肺炎")
jieba.add_word("钻石公主号")
jieba.add_word("华南海鲜市场")

def preProcess(word):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    result = re.sub(pattern, '', word)
    if len(result) > 0:
        return ",".join(jieba.cut(result))
    return result

def getCorpus(fileName, page):
    print(fileName)
    # fin = open('originalData\\' + fileName+ '\\' + fileName + 'Page' + str(page) + ".txt", "r", encoding='utf-8')
    fin = open('crawl_files/'+fileName+'/'+ fileName + 'Page' + str(page) + '.txt', 'r', encoding='utf-8')
    lines = fin.readlines()
    # print(lines)
    newLines = []
    corpus = []
    for line in lines:
        # print(line)
        if line == '*\n':
            text = [word for word in newLines if word not in stopWords]
            corpus.append(text)
            newLines = []

        newLine = []
        line = re.split('。|，|！|？|：|（|）|；|”|“|《|》|、', line)
        print('re.split line:', line)
        for word in line:
            # print(word)
            newWord = preProcess(word)
            print("preprocess word:", newWord)
            if len(newWord) > 0:
                newLine += newWord.split(",")
        # print(newLine)
        if len(newLine) > 0:
            newLines += newLine
        # print(newLines)
    # print(newLines)
    # print(len(corpus))
    # print(corpus)
    return [' '.join(c) for c in corpus]


def cleanData(paper, num):
    # fout = open('data\\' + paper+'.txt', 'w')
    for page in range(1, num+1, 1):
        corpus = getCorpus(paper, page)
        print('++++++++++++++++corpus is :', corpus)
        # fout.write('\n'.join(corpus))
        # fout.write('\n')


cleanData('renmin', 1)
# cleanData('xinhua', 26)
# cleanData('huanqiu', 31)
# cleanData('guancha', 28)
# cleanData('wenhui', 26)
# cleanData('chinadaily', 23)
# cleanData('sputniknews', 32)
# cleanData('WSJ', 35)
# cleanData('NTY', 56)
# cleanData('DW', 1)
# cleanData('BBC', 29)
