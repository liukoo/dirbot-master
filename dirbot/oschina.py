# -*- coding:utf-8 -*-
# 抓取oschina 博客
import re,httplib2
url ="http://www.oschina.net/blog/more?p=1"
http = httplib2.Http()
headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5"}
#rule = re.compile(r'<li><a.*search.jsp\?N=(.*)\'>(.*)</a>')
rule = re.compile(r"<h3><a href=\"(.*)\".*>(.*)</a></h3>\s*<p>(.*)</p>")
for i in range(1,26):
    url ="http://www.oschina.net/blog/more?p="+str(i)
    response, content = http.request(url, 'GET',headers=headers)
    m = rule.findall(content)
    if m:
        for i in m:
            temp=""
            print i[0].strip()
            for j in range(len(i[2].strip())):
                temp +='-'
            print temp


