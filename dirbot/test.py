#coding:utf-8
import re,httplib2,chardet,MySQLdb
import time
url1 = 'http://test.com/taobao.htm'
url = "http://tbskip.taobao.com/json/show_buyer_list.htm?bid_page=1&page_size=15&is_start=false&item_type=b&ends=1366211729000&starts=1365606929000&item_id=17009274899&user_tag=34672672&old_quantity=11474&zhichong=true&seller_num_id=1119339412&dk=&isFromDetail=yes&totalSQ=12237&sbn=a9d6b6a17b6ed27f89dfbc926c0c25f5"
http = httplib2.Http()
headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5"}
response, content = http.request(url, 'GET',headers=headers)
html = content
code =  chardet.detect(html)['encoding'].lower()
if code =='utf-8':
    html = html.decode('utf-8')
else:
    html = html.decode('gbk')
count_money = 0
count_num =0
#匹配货号
rule1 = re.compile(r"item_id=(\d+)")
#匹配成交记录
rule2 = re.compile(r"detail:params=\"(.*),")
#匹配拍下价格
rule3 = re.compile(r"<em>(\d+)</em>")
#匹配拍下数量
rule4 = re.compile(r"<td>(\d+)</td>")
#匹配拍下时间
rule5 = re.compile(r"<td>(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})</td>")
#匹配下一页成交记录
rule6 = re.compile(r"detail:params=\"(.*),.*page-next\"><span>")
#匹配下一页页码
rule7 = re.compile(r"bid_page=(\d*)")
rule8 = re.compile(r"bidPage=(\d*)")
Count =[]
Num = []
page=[1,2,49,50,98,99]
while True:
    if not page:
        break
    page_index = page.pop()
    page_number = rule7.search(url)
    if not page_number:
        page_number = rule8.search(url)
    page_number = int(page_number.group(1))
    url = url.replace("bidPage="+str(page_number),"bidPage="+str(page_index))
    if page_number > 111:
        break
    response, html = http.request(url, 'GET',headers=headers)
    code =  chardet.detect(html)['encoding'].lower()
    if code =='utf-8':
        html = html.decode('utf-8')
    else:
        html = html.decode('gbk')
    #遍历价格、数量
    number = rule4.findall(html)
    price = rule3.findall(html)
    time1 = rule5.findall(html)
    number = [int(i) for i in number]
    price = [int(i) for i in price]
    Count.extend(price)
    Num.extend(number)
    for i in number:
        count_money+=i*price.pop()
        count_num+=i
    ####
    next_page = rule6.search(html)
    #是否存在下一页
    if not next_page:
        print page_number
        break
    url = next_page.group(1).replace("&amp;","&")
    time.sleep(1.5)
print Count
print Num
a = [Count[i] for i in range(len(Count)) if Count[i] not in Count[:i]]
result = {}
for money in a:
    result[money]= 0
    index =0
    for num in Count:
        if num==money:
            result[money] += Num[index]
print result