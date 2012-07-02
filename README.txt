1、seg_text方法主要是分词使用。
eg:
import scseg
scseg.seg_text(u'研究生命起源')
scseg.seg_text(u'第四十七中学')

2、keywords是生成关键字使用，列出所有的分词可能。
import scseg
scseg.keywords(u'研究生命起源')

3、另外提供个自学习的小工具，可以根据文本提取词组。主要是根据两个字相邻并且出现的概率来作为主要依据。
