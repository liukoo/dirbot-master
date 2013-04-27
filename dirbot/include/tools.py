import chardet
def conv(str):
    #return str.decode('gbk')
    code =  chardet.detect(str)['encoding'].lower()
    if code =='utf-8':
        str = str.decode('utf-8')
    else:
        str = str.decode('gbk')
    return str
