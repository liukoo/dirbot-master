#coding:utf-8
import httplib2,re
from tools import conv
p_url = re.compile(r"<a href=\"http://a\.m\..*/i(.*)\.htm") #匹配商品链接
item_list = re.compile(ur"data-url=\"(.*)\u6240\u6709\u5b9d")  #匹配所有宝贝链接
price1 = re.compile(r"\"promoPrice\":\"(\d*\.\d*)")  #促销价
price2 = re.compile(r"\"price\":\"(\d*\.\d*)")   #原价
price3 = re.compile(r"price: \".(\d*\.\d*)\"")
sales  = re.compile(ur"(\d*) \u4ef6")  #匹配销量
pid = re.compile(r"\"item_id\" value=\"(\d*)\"")  #匹配商品ID
b_shopid = re.compile(r"shop_id=(\d*)&amp")  #商城店铺ID
c_shopid = re.compile(r"shop=(\d*)\.m")      #C店店铺ID
next_page = re.compile(r"c-pnav-next\">\r\n<a href=\"(.*)\"") #下一页
web = httplib2.Http()
r,c = web.request("http://a.m.taobao.com/i16516584593.htm", 'GET',headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31"})
html = conv(c)
print price3.search(html).group(1)
#print html
#print price2.search(html).group(1)
#print item_list.findall(html)[0].replace("&amp;","&").replace('">',"")
#print rule.findall(html)
#print sales.search(html).group(1)
