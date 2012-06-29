#encoding:utf-8
import os
import re
from route.mmseg import route
from .word import Word,Dictionary

here = os.path.abspath(os.path.dirname(__file__))
dict_words = Dictionary(here+os.sep+'data')


class Chunk(object):

    def __init__(self,*words):
        self.words = words
    
	#计算chunk的总长度
    def total_word_length(self):
        length = 0
        for word in self.words:
            length += len(word.text)
        return length
    
	#计算平均长度
    def average_word_length(self):
        return float(self.total_word_length()) / float(len(self.words))

    #统计词频
    def word_frequency(self):
        sum = 0
        for word in self.words:
            sum += word.freq
        return sum
    
	#计算标准差
    def standard_deviation(self):
        average = self.average_word_length()
        sum = 0.0
        for word in self.words:
            tmp = (len(word.text) - average)
            sum += float(tmp) * float(tmp)
        return sum


regex = u'[a-zA-Z0-9_]+[*?]*|[\u4E00-\u9FFF\u3400-\u4dbf\uf900-\ufaff\u3040-\u309f\uac00-\ud7af]+[*?]*'
find_glob  = re.compile(regex, re.UNICODE).findall
class Splitter(object):  
      
    def __init__(self,text,route=route): 
        self.text = text  
        self.pos = 0  
        self.text_length = len(self.text)  
        self.route = route  
              
    def next_char(self):  
        return self.text[self.pos]  
          
    #判断该字符是否是中文字符（不包括中文标点）    
    def is_cjk_char(self,charater):  
        c = ord(charater)
        return 0x4E00<= c <=0x9FFF or\
               0x3400<= c <=0x4dbf or\
               0xf900<= c <=0xfaff or\
               0x3040<= c <=0x309f or\
               0xac00<= c <=0xd7af

    #判断是否是ASCII码  
    def is_latin_char(self, ch):  
        import string  
        if ch in string.whitespace:  
            return False  
        if ch in string.punctuation:  
            return False  
        return ch in string.printable  
      
    #得到下一个切割结果  
    def __iter__(self):  
        while self.pos < self.text_length:  
            if self.is_cjk_char(self.next_char()):  
                for token in self.get_cjk_words():
                    if token > 0:
                        word = unicode(token)
                        if word != 'X':
                            yield word
            else :  
                token = self.get_latin_words() 
                if len(token) > 0:  
                    yield unicode(token)  
        raise StopIteration
      
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
        return self.text[start:end]  
      
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
            self.pos += len(word1.text)  
            if self.pos < self.text_length:  
                words2 = self.get_match_cjk_words()  
                for word2 in words2:  
                    self.pos += len(word2.text)  
                    if self.pos < self.text_length:  
                        words3 = self.get_match_cjk_words()  
                        for word3 in words3:  
                            if word3.length == -1:  
                                chunk = Chunk(word1,word2)  
                            else :  
                                chunk = Chunk(word1,word2,word3)  
                            chunks.append(chunk)  
                    elif self.pos == self.text_length:  
                        chunks.append(Chunk(word1,word2))  
                    self.pos -= len(word2.text)  
            elif self.pos == self.text_length:  
                chunks.append(Chunk(word1))  
            self.pos -= len(word1.text)  
                                  
        self.pos = originalPos  
        return chunks  
      
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
                  
        self.pos = originalPos  
        if not words:  
            word = Word()  
            word.length = -1  
            word.text = 'X'  
            words.append(word)  
        return words

    def keywords(self):
        words = set()
        for item in find_glob(self.text):
            if self.is_latin_char(item[0]):
                words.add(item)
            else:
                max_length = len(item)
                for i in range(max_length):
                    for j in range(i,max_length):
                        word=dict_words[item[i:j+1]]
                        if word and len(word)>1:
                            words.add(unicode(word))
        return words
