#encoding:utf-8

from scseg import seg_text
from scseg.word import Dictionary


class Learning(object):
    
    def __init__(self,times=3,train = None):
        self.cache = {}
        self.times = times
        if train:
            del Dictionary.dict_words 
            Dictionary.dict_words= {}
            Dictionary.load(train)

    def learn(self,path):
        """
        待学习的文件路径
        """
        count = 0
        for line in open(path):
            count = count +1
            line = unicode(line,'utf-8')
            tmp = []
            for word in seg_text(line):
                if len(word) == 1:
                    tmp.append(word)
                else:
                    if len(tmp)>1:
                        new_word=''.join(tmp)
                        if new_word in self.cache:
                            self.cache[new_word] = self.cache[new_word]+1
                        else:
                            self.cache[new_word] = 1
                    del tmp
                    tmp = []
            new_word = ''.join(tmp)
            if new_word:
                if new_word in self.cache:
                    self.cache[new_word] += 1
                else:
                    self.cache[new_word] = 1
            if count%1000 == 0:
                print("count:%d" % count)
    def save(self,path):
        with open(path,'w') as f:
            for word in self.cache.viewitems():
                if word[1]>=self.times:
                    f.write('%s\t%s\n' % (word[0].encode("utf-8"),word[1]))
