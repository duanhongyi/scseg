#encoding:utf-8
import re

CN_NUM = {
u'〇' : 0,
u'一' : 1,
u'二' : 2,
u'三' : 3,
u'四' : 4,
u'五' : 5,
u'六' : 6,
u'七' : 7,
u'八' : 8,
u'九' : 9,

u'零' : 0,
u'壹' : 1,
u'贰' : 2,
u'叁' : 3,
u'肆' : 4,
u'伍' : 5,
u'陆' : 6,
u'柒' : 7,
u'捌' : 8,
u'玖' : 9,

u'貮' : 2,
u'两' : 2,
}
CN_UNIT = {
u'十' : 10,
u'拾' : 10,
u'百' : 100,
u'佰' : 100,
u'千' : 1000,
u'仟' : 1000,
u'万' : 10000,
u'萬' : 10000,
u'亿' : 100000000,
u'億' : 100000000,
u'兆' : 1000000000000,
}


has_unit  = re.compile((u'+[*?]*|'.join(CN_UNIT.keys())), re.UNICODE).findall

chinese_number_regex =  '^['+u''.join(CN_UNIT.keys()+CN_NUM.keys())+']+$'
is_number = re.compile(chinese_number_regex,re.UNICODE).match


def chinese_to_number(cn):
    if has_unit(cn):
        lcn = list(cn)
        unit = 0 #当前的单位
        ldig = []#临时数组
        while lcn:
            cndig = lcn.pop()
            if CN_UNIT.has_key(cndig):
                unit = CN_UNIT.get(cndig)
                if unit==10000:
                    ldig.append('w')    #标示万位
                    unit = 1
                elif unit==100000000:
                    ldig.append('y')    #标示亿位
                    unit = 1
                elif unit==1000000000000:#标示兆位
                    ldig.append('z')
                    unit = 1
                continue
            else:
                dig = CN_NUM.get(cndig)
                if unit:
                    dig = dig*unit
                    unit = 0
                ldig.append(dig)
        if unit==10:    #处理10-19的数字
            ldig.append(10)
        ret = 0
        tmp = 0
        while ldig:
            x = ldig.pop()
            if x=='w':
                tmp *= 10000
                ret += tmp
                tmp=0
            elif x=='y':
                tmp *= 100000000
                ret += tmp
                tmp=0
            elif x=='z':
                tmp *= 1000000000000
                ret += tmp
                tmp=0
            else:
                tmp += x
        ret += tmp
        return ret
    else:
        return int(''.join([str(CN_NUM[c]) for c in cn]))
