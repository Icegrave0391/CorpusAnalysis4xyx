import re

class Tool:
    removeImg = re.compile('<img.*?>| {7}|')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()

tool = Tool()

def save():
    fin = open('./BBC/BBCPage1.txt', "r", encoding='utf-8')
    lines = fin.readlines()
    for line in lines:
        if(line != '*\n'):
            line = tool.replace(line)
            print(line)
        else:
            print("--------NEXT----------")

# main()
if __name__ == "__main__":
    src_prefix = '../crawl_files/'
    dst_prefix = '../crawl2raw_files'
    src_list = ['BBC', 'chinadaily', 'DW', 'huanqiu', 'NTY', 'renmin']
    src_pages = [19, 22, 1, 30, 56, 27]
    for i, srcname in enumerate(src_list):
        num_pages = src_pages[i]
        print(num_pages)
        for j in range(num_pages):
            idx = j+1
            print(src_prefix + srcname + '/' + srcname + 'Page' + str(idx))



        # fin = open(src_prefix + srcname + '/' + srcname + 'Page' +)
