import pprint
import logging
import os
import collections
from gensim import models
from gensim import corpora
from collections import defaultdict
from gensim import similarities
from gensim.test.utils import datapath
import pyLDAvis.gensim

pardir = os.path.abspath(os.path.join(os.path.dirname('CorpusTool.py'), os.path.pardir)) + '/'
corpPrefix_default = pardir + 'corpus_files/'
class TopicAnalysisModel(object):
    """
    Tool for corpus analysis
    """
    def __init__(self, corpPrefix=corpPrefix_default):
        self.params = {}
        self.params['corpPrefix'] = corpPrefix
        self.params['corplist'] = ['BBC', 'chinadaily', 'DW', 'huanqiu', 'NTY', 'renmin', 'sputniknews', 'CNR']
        self.params['pglist'] =   [  19 ,      22     ,   1 ,     30   ,   56 ,    27   ,      30      ,  426]

    def read_corpus(self):
        for i in range(len(self.params['corplist'])):
            fpath = self.params['corpPrefix'] + self.params['corplist'][i] + '.txt'
