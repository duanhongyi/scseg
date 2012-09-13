#encoding:utf-8
#词典
import os
from scseg.digital import is_chinese_number

#单个词实体映射
class Word(object):

    def __init__(self,text = '',freq = 0,length = -1):
        self.text = text#词
        self.freq = freq#词频
        self.length = len(text) if length<0 else length#有效词长

    def __str__(self):
        return self.text
    
    def __repr__(self):
        return self.text

    def __len__(self):
        return self.length

class Dictionary(object):

    dict_words = {}

    def __init__(self,root_path):
        #载入字库
        if not Dictionary.dict_words:
            for path in os.listdir(root_path): 
                if path.endswith('.dic'):
                    self.load(os.sep.join([root_path,path]))

    @staticmethod
    def load(path):
        """
        载入字典
        """
        for line in open(path):
            words = line.split(' ')
            if len(words)==2:
                word = unicode(words[0].strip(), 'utf-8')
                Dictionary.dict_words[word] = Word(word, int(words[1]))
            elif len(words)==1:
                word = unicode(words[0].strip(),'utf-8')
                Dictionary.dict_words[word] = Word(word,0)

    def __len__(self):
        return len(self.dict_words)

    def __getitem__(self,word):
        if Dictionary.dict_words.has_key(word):
            return Dictionary.dict_words[word]
        elif is_chinese_number(word):#数字识别
            return Word(word,0)
        elif len(word) == 1:#生僻字词频为0
            return Word(word,0)
        else:
            return None

