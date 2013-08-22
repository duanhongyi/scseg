scseg
========
scseg中文分词，是基于mmseg的简单分词组件


Feature
========
* 支持pinyin分词
* 支持用户自定义词典
* 支持单位合并
* 支持汉字数字识别

Install
==========
* `pip install scseg`
* 通过`import scseg`来引用


Algorithm
==========
* 采用mmseg算法进行切分
* 采用规则方式支持中文数字分词

功能 1)：分词`scseg.seg_text`方法
==============

* `scseg.seg_text`函数接受3个参数: 
* `text`参数为需要分词的字符 
* `ext_dict_words`为用户自定义的扩展字典
* `use_combine`代表是否需要合并处理

代码示例( 全功能分词 )

    #encoding=utf-8
    import genius

    seg_list = scseg.seg_text(u'中国人民站起来了pinyin')
    print '\n'.join(seg_list)


功能 2)：面向索引的分词
==============
* `scseg.seg_keywords`为面向索引的切割方式
* 其作用是枚举出所有可能的切割方式
* `text`参数为需要分词的字符 

代码示例( 全功能分词 )

    #encoding=utf-8
    import scseg

    seg_list = scseg.seg_keywords(u'中国人民站起来了pinyin')
    print '\n'.join(seg_list)
