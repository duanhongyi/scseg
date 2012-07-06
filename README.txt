1、seg_text方法主要是分词使用。可以调用scseg包下的seg_text方法进行分词。例如：seg_text(u'第四十七中学')

2、keywords是生成关键字使用，列出所有的分词可能，此功能是做term时候防止漏词而设计，可以枚举出所有的分词结果。例如：keywords(u'研究生命起源')

3、另外提供个自学习的小工具，可以根据文本提取词组。提供个以\n字符作为分割的语料，输入learn命令，即可以学习出词组。

4、learn命令说明：learn 3 /home/xxx/corpus.txt /home/xxx/save_file.txt,其中3代表出现的次数，即两个字连续出现次数大于3次的我们认为是一个词。/home/xxx/corpus.txt代表的是语料库的位置，/home/xxx/save_file.txt代表的是学习结果存储的位置。

5、用户可以自定义词库，只需将词库的扩展名为dic，的文件放入scseg/data目录下即可，格式参考原有词库。也可以调用word模块下Dictionary的load函数，自定义词典目录位置。
