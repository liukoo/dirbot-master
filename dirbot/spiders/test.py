#coding:utf-8
import re,httplib2,chardet,MySQLdb
def iconv(str):
    code = chardet.detect(str)['encoding'].lower()
    if code=="utf-8":
        str = str.decode('utf-8')
    else:
        str = str.decode('gbk')
    return str

b=[1,1,1]
a =["1","2","2"]
for i in b:
    if a.pop()!="0":
        print 1
