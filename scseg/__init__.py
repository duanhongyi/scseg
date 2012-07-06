#encoding:utf-8

import chardet
from .core import Splitter,Keywords
from .route.mmseg import route

def seg_text(text):
    if not isinstance(text,unicode):
        encoding = chardet.detect(text)['encoding']
        text = unicode(text,encoding)
    return [word for word in Splitter(text)]

def keywords(text):
    #制作关键词,联合单个字
    if not isinstance(text,unicode):
        encoding = chardet.detect(text)['encoding']
        text = unicode(text,encoding)
    words = Keywords(text)
    return [word for word in words]
