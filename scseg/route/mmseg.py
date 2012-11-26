#encoding:utf-8

class Router(object):
    
    def compare(self,chunks,comparator):
        """
        chunk选择器
        """
        i = 1
        for j in range(1, len(chunks)):
            rlt = comparator(chunks[j], chunks[0])
            if rlt > 0:
                i = 0
            if rlt >= 0:
                chunks[i], chunks[j] = chunks[j], chunks[i]
                i += 1
        return chunks[0:i]
    

    def __call__(self,chunks):
        """
        选择chunks
        """
        chunks = self.maximum_matching(chunks)
        if len(chunks) > 1:
            chunks = self.largest_average(chunks)
        if len(chunks) > 1:
            chunks = self.smallest_variance(chunks)
        if len(chunks) > 1:
            chunks = self.effective_count(chunks)
        if len(chunks) > 1:
            chunks = self.morphemic_freedom(chunks)
        return chunks

    def maximum_matching(self,chunks):
        """
        最大匹配
        """
        def comparator(a,b):
            return a.total_word_length() - b.total_word_length()
        return self.compare(chunks,comparator)

    def largest_average(self,chunks):
        """
        单词的最大平均长度
        """
        def comparator(a,b):
            return a.average_word_length() - b.average_word_length()
        return self.compare(chunks,comparator)

    def smallest_variance(self,chunks):
        """
        词语长度的最小变化率
        """
        def comparator(a,b):
            return b.standard_deviation() - a.standard_deviation()
        return self.compare(chunks, comparator)

    def effective_count(self, chunks):
        """
        有效词数量
        """
        def comparator(a,b):
            return a.effective_word_number() - b.effective_word_number()
        return self.compare(chunks, comparator)
    
    def morphemic_freedom(self,chunks):
        """
        计算词组中的所有单字词词频的自然对数,
        然后将得到的值相加，取总和最大的词组。
        """
        
        def comparator(a,b):
            return a.word_frequency() - b.word_frequency()
        return self.compare(chunks, comparator)

route = Router()
