#encoding:utf-8

import chardet
from .core import Splitter
from .route.mmseg import route

def seg_text(text, ext_dict_words = set()):
    if not isinstance(text,unicode):
        encoding = chardet.detect(text)['encoding']
        text = unicode(text,encoding)
    return [word for word in Splitter(text, ext_dict_words)]
