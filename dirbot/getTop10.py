#coding:utf-8
import re,httplib2,chardet,MySQLdb
def iconv(str):
    code = chardet.detect(str)['encoding'].lower()
    if code=="utf-8":
        str = str.decode('utf-8')
    else:
        str = str.decode('gbk')
    return str
url = "http://list.tmall.com/search_product.htm?active=1&area_code=320000&search_condition=16&vmarket=0&style=w&sort=s&n=60&s=0&cat=50025829"
http = httplib2.Http()
s,c = http.request(url,'GET',None,None,100)
c = iconv(c)
rule = re.compile(r"data-p=\"\d+-2\">(.*)</a>")
rule1 = re.compile(r"data-current=\"([^\"]*)")
stores = rule.findall(c)
store_url =re.compile(r"shopHeader-enter\">\s\n<a href=\"(.*)\" atpanel").findall(c)
top10 = {}
index =0
for name in stores[:10]:
    top10[name] = store_url[index]
    index +=1
for key in top10:
    s,c = http.request(top10[key],'GET',None,None,100)
    c = iconv(c)
    top10[key] = rule1.search(c).group(1)

conn=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306,charset='utf8')
cur=conn.cursor()
conn.select_db('python')
##写入数据库
for key in top10:
    value = []
    value.append(key)
    value.append(top10[key])
    sql = "insert into task_list(name,url) values(%s,%s)"
    cur.execute(sql,value)
    conn.commit()

conn.close()