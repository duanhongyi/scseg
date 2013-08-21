#encoding:utf-8

import chardet
from .core import Splitter, KeywordsSplitter
from .route.mmseg import route
from .quantifier import combine_quantifier


def seg_text(text, ext_dict_words = set(), use_combine = True):
    if not isinstance(text,unicode):
        encoding = chardet.detect(text)['encoding']
        text = unicode(text,encoding)
    result = [word for word in Splitter(text, ext_dict_words)]
    if use_combine == True:
        return combine_quantifier(result)
    return result

def seg_keywords(text):
    return KeywordsSplitter(text).__iter__()
