import re
from scseg.word import Dictionary
from scseg.digital import is_chinese_number

number_pattern = u'[0-9]+[*?]*'


def combine_quantifier(words):
    pos = 0
    words_length = len(words)
    result = []
    while pos < words_length:
        word1 = words[pos]
        if (re.match('^%s$' % number_pattern, word1) or\
            is_chinese_number(word1)) and pos < words_length -1:
                word2 = words[pos+1]
                if word2 in Dictionary.quantifier_words:
                    result.append(word1+word2)
                    pos += 2
                    continue
        result.append(word1)
        pos += 1
    return result
