#encoding:utf-8
import scseg

def test_seg():
    seg_words=scseg.seg_text(u'研究生命起源')
    assert seg_words[0] == u'研究'
    assert seg_words[1] == u'生命'
    assert seg_words[2] == u'起源'
