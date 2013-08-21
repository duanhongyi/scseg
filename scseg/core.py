#encoding:utf-8
import os
import re
import string
from route.mmseg import route
from .word import Word, Dictionary


here = os.path.abspath(os.path.dirname(__file__))
dict_words = Dictionary(here+os.sep+'data')
group_char = re.compile(u'[a-zA-Z]+[*?]*|[0-9]+[*?]*|.+[*?]*', re.UNICODE).findall


class Chunk(object):

    def __init__(self, *words):
        self.words = []
        for word in words:
            if len(word) == 0:
                continue
            self.words.append(word)
    
	#计算chunk的总长度
    def total_word_length(self):
        length = 0
        for word in self.words:
            length += len(word)
        return length
    
	#计算平均长度
    def average_word_length(self):
        return float(self.total_word_length()) / float(len(self.words))

    #统计有效词数
    def effective_word_number(self):
        _sum = 0
        for word in self.words:
            if len(word) > 1 and word.freq >=0:
                _sum += 1
        return _sum

    #统计词频
    def word_frequency(self):
        _sum = 0
        for word in self.words:
            _sum += word.freq
        return _sum
    
	#计算标准差
    def standard_deviation(self):
        average = self.average_word_length()
        _sum = 0.0
        for word in self.words:
            tmp = (len(word) - average)
            _sum += float(tmp) * float(tmp)
        return _sum



class BaseSplitter(object):
    
    def __init__(self, text, ext_dict_words=set()): 
        self.text = text  
        self.pos = 0
        self.text_length = len(self.text)  
        self.ext_dict_words = ext_dict_words
    
    def next_char(self):  
        return self.text[self.pos]  

    @staticmethod
    def is_cjk_char(charater):  
        c = ord(charater)
        return 0x4E00 <= c <= 0x9FFF or\
               0x3400 <= c <= 0x4dbf or\
               0xf900 <= c <= 0xfaff or\
               0x3040 <= c <= 0x309f or\
               0xac00 <= c <= 0xd7af
    
    #判断是否是ASCII码
    @staticmethod
    def is_latin_char(ch):  
        if ch in string.whitespace:  
            return False  
        if ch in string.punctuation:  
            return False  
        return ch in string.printable  

    #切割出非中文词  
    def get_latin_words(self):  
        # Skip pre-word whitespaces and punctuations  
        #跳过中英文标点和空格  
        while self.pos < self.text_length:  
            ch = self.next_char()  
            if self.is_latin_char(ch) or self.is_cjk_char(ch):  
                break  
            self.pos += 1  
        #得到英文单词的起始位置      
        start = self.pos  
          
        #找出英文单词的结束位置  
        while self.pos < self.text_length:  
            ch = self.next_char()  
            if not self.is_latin_char(ch):  
                break  
            self.pos += 1  
        end = self.pos  
          
        #Skip chinese word whitespaces and punctuations  
        #跳过中英文标点和空格  
        while self.pos < self.text_length:  
            ch = self.next_char()  
            if self.is_latin_char(ch) or self.is_cjk_char(ch):  
                break  
            self.pos += 1  
              
        #返回英文单词  
        return Word(self.text[start:end])

    #运用正向最大匹配算法结合字典来切割中文文本    
    def get_match_cjk_words(self):  
        originalPos = self.pos  
        words = []  
        index = 0  
        while self.pos < self.text_length:  
            if index >= len(dict_words) :  
                break  
            if not self.is_cjk_char(self.next_char()):
                break  
            self.pos += 1  
            index += 1  
              
            text = self.text[originalPos:self.pos]  
            word = dict_words[text]  
            if word:  
                words.append(word)
            elif text in self.ext_dict_words:
                words.append(Word(text, -1))
                  
        self.pos = originalPos  
        if not words:
            words.append(Word('X', 0, 0))#添加结束词 
        return words


class Splitter(BaseSplitter):  
      
    def __init__(self, text, ext_dict_words=[], route=route):
        BaseSplitter.__init__(self, text, ext_dict_words)  
        self.route = route  
      
    #得到下一个切割结果  
    def __iter__(self):  
        while self.pos < self.text_length:  
            if self.is_cjk_char(self.next_char()):  
                for word in self.get_cjk_words():
                    if len(word) > 0:
                        word = unicode(word)
                        yield word
            else :  
                word = self.get_latin_words() 
                if len(word) > 0:
                    for word in group_char(unicode(word)):
                        yield word 
        raise StopIteration
      
    #切割出中文词，并且做处理，用上述4种方法  
    def get_cjk_words(self):  
        #应用规则过滤
        chunks = self.route(self.create_chunks())
          
        #最后只有一种切割方法  
        chunk = chunks[0] 
        self.pos += chunk.total_word_length()  
        return chunk.words
      
    #三重循环来枚举切割方法，这里也可以运用递归来实现  
    def create_chunks(self):  
        chunks = []  
        originalPos = self.pos  
        words1 = self.get_match_cjk_words()  
          
        for word1 in words1:  
            self.pos += len(word1)  
            if self.pos < self.text_length:  
                words2 = self.get_match_cjk_words()  
                for word2 in words2:  
                    self.pos += len(word2)  
                    if self.pos < self.text_length:  
                        words3 = self.get_match_cjk_words()  
                        for word3 in words3:  
                            chunk = Chunk(word1, word2, word3)  
                            chunks.append(chunk)  
                    elif self.pos == self.text_length: 
                        chunks.append(Chunk(word1, word2))  
                    self.pos -= len(word2)  
            elif self.pos == self.text_length:
                chunks.append(Chunk(word1))  
            self.pos -= len(word1)  
        self.pos = originalPos
        return chunks


class KeywordsSplitter(Splitter):

    def __iter__(self):
        pre_words = set([word for word in Splitter.__iter__(self)])
        return pre_words.union(self.keywords())

    def keywords(self):
        text = self.text
        pos, length = 0, len(text)
        pre_words = set()
        while pos < length:
            for i in range(pos + 1, length + 1):
                pre_word = text[pos:i]
                if dict_words[pre_word] and len(pre_word) > 1:
                    pre_words.add(pre_word)
            pos += 1
        return pre_words
