import re
import os

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

# main()
if __name__ == "__main__":
    # path prefix
    pardir = os.path.abspath(os.path.join(os.path.dirname('crwal2text.py'), os.path.pardir)) + '/'
    src_prefix = pardir + 'crawl_files/'
    dst_prefix = pardir + 'crawl2raw_files/'
    file_suffix = '.txt'
    src_list = ['BBC', 'chinadaily', 'DW', 'huanqiu', 'NTY', 'renmin', 'sputniknews', 'CNR']
    src_pages =[ 19  ,      22     ,  1  ,    30    ,  56  ,    27   ,      30      ,  426 ]
    for i, srcname in enumerate(src_list):
        num_pages = src_pages[i]
        print(num_pages)
        for j in range(num_pages):
            idx = str(j+1)
            srcp = src_prefix + srcname + '/' + srcname + 'Page' + idx + file_suffix
            dstp = dst_prefix + srcname + '/' + srcname + 'Page' + idx + file_suffix
            print(src_prefix + srcname + '/' + srcname + 'Page' + idx)
            # file operation -- src file resolveing
            fin = open(srcp, 'r', encoding='utf-8')
            fout = open(dstp, 'w')
            lines = fin.readlines()
            title_tag = 0
            for i, line in enumerate(lines):
                if i == 0:
                    fout.write('>>>' + line + '\n')
                else:
                    if(line == '\n'):
                        pass
                    if(line == '*\n'):
                        line = '\n===========NEXT NEWS==========\n\n'
                        fout.write(line)
                        title_tag = 1
                    elif(line != '*\n'):
                        line = tool.replace(line) + '\n'
                        if(title_tag):
                            title_tag = 0
                            fout.write('>>>' + line + '\n')
                        else:
                            fout.write(line)



