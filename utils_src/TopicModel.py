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
        self.params['newssizelist'] = [] # definited by reading process
        self.glbcorpus = None
        self.corpdict = None
        self.bowcorpus = None

    def read_corpus(self):
        """
        Method for reading all corpus files in corpus_files/..
        Setter for self.glbcorpus : list (len = number of total news in all news files)
        """
        glbcorpus = []
        glbwords = 0
        glbarticles = 0
        print(">>> [file process] Start processing corpus files")
        for i in range(len(self.params['corplist'])):
            fpath = self.params['corpPrefix'] + self.params['corplist'][i] + '.txt'
            fin = open(fpath, 'r')
            # print('>>>> Start reading corpus file: ', fpath)
            # read file
            lines = fin.readlines()
            print('[' + self.params['corplist'][i] + ']' + ' article size: ', len(lines),
                  ', words: ', sum([len(line.split(' ')) for line in lines]))
            # data handle
            self.params['newssizelist'].append(len(lines))
            glbarticles += len(lines)
            glbwords += sum([len(line.split(' ')) for line in lines])
            glbcorpus += [line[:-1] for line in lines]
        print(glbcorpus[0])
        print('newssizelist:' ,self.params['newssizelist'])
        #print([document.split(' ') for document in glbcorpus])
        self.glbcorpus = [document.split(' ') for document in glbcorpus]

    def corpus2bow(self, corpus=None):
        print('>>> Start corpus -> bow process')
        if corpus == None:
            corpus = self.glbcorpus
        # word <-> id
        corpdictionary = corpora.Dictionary(corpus)
        # filter words with extreme frenquency
        self.corpdict = corpdictionary
        self.corpdict.filter_extremes(no_below=20, no_above=0.5)
        self.bowcorpus = [corpdictionary.doc2bow(doc) for doc in corpus]
        print('Number of unique tokens %d' % len(self.corpdict))
        print('Number of documents %d' % len(self.bowcorpus))

    def LDA(self, corpdictionary=None, bowcorpus=None, num_topics=5, random_state=100, iterations=400, passes=20, alpha='auto', eta='auto'):
        if corpdictionary == None:
            corpdictionary = self.corpdict
        if bowcorpus == None:
            bowcorpus = self.bowcorpus
        # print('dic:', corpdictionary)
        temp = corpdictionary[0] # only to load dictionary
        id2word = corpdictionary.id2token
        print('tokens:', id2word)
        chunksize = len(bowcorpus)
        print(">>> Start LDA Modeling")
        LDAModel = models.LdaModel(
            corpus=bowcorpus,
            id2word=id2word,
            chunksize=chunksize,
            random_state=random_state,
            iterations=iterations,
            num_topics=num_topics,
            passes=passes,
            eval_every=None,
            alpha=alpha,
            eta=eta
        )
        temp_file = datapath('model')
        LDAModel.save(temp_file)
        LDAModel.print_topics()
        top_topics = LDAModel.top_topics(bowcorpus)  # , num_words=20)

        # Average topic coherence is the sum of topic coherences of all topics, divided by the number of topics.
        avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
        print('Average topic coherence: %.4f.' % avg_topic_coherence)
        pprint.pprint(top_topics)
        # visulization
        vis = pyLDAvis.gensim.prepare(LDAModel, bowcorpus, corpdictionary)
        pyLDAvis.save_html(vis, 'lda.html')

if __name__ == '__main__':
    model = TopicAnalysisModel()
    model.read_corpus()
    model.corpus2bow()
    model.LDA()