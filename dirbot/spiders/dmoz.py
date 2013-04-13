# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
import re,chardet,time,MySQLdb,httplib2
from dirbot.items import Website
class DmozSpider(CrawlSpider):
    name = "taobao"
    allowed_domains = ["tmall.com","taobao.com"]
    ####################################################################################################################
    #匹配商品列表页的下一页
    r_pro_list_page = re.compile(r"J_SearchAsync next\" href=\"(.*)\"")
    #匹配商品列表页中商品名称、ID
    r_pro_list_item = re.compile(r"detail.tmall.com/item.htm\?id=(\d+)&\" class=\"permalink\" style=\"\">\n+(.*)\n+</a>")
    #匹配商品列表页中商品的销量
    r_pro_list_sell_count = re.compile(r"<em>(\d+)</em>")

    #匹配商品详情页中init的地址 url
    r_init_url = re.compile(r"initApi\" : \"(.*)\",")
    #配置商品init url中的月成交数量
    r_sell_count = re.compile(r"sellCount\":(\d+)}")
    #匹配商品详情页中的商品ID
    r_pro_id = re.compile(r"itemId:\"(\d+)\"")
    #匹配商品详情页中商品名称
    r_pro_name = re.compile(r"\"title\":\"(.*)\"")
    #匹配商品详情页的商品价格
    r_pro_price = re.compile(r"reservePrice\' : \'(.*)\'")
    #匹配商品详情页的成交记录URL
    r_pro_buyer_list = re.compile(r"detail:params=\"(.*),")

    #匹配成交记录中的商品ID
    r_buyer_id = re.compile(r"item_id=(\d+)")
    #匹配成交记录页面的下一页URL
    r_buyer_page = re.compile(r"detail:params=\"(.*),.*page-next\"><span>")
    #匹配成交记录页面中的拍下价格
    r_buyer_price = re.compile(r"<em>(\d+)</em>")
    #匹配拍下的数量
    r_buyer_number = re.compile(r"<td>(\d+)</td>")
    #匹配成交记录当前页的页码
    r_buyer_cur_page = re.compile(r"page-cur\">(\d+)<")


    ####################################################################################################################
    #开始
    def start_requests(self):
        self.http =httplib2.Http()
        self.conn=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306,charset='utf8')
        self.cur=self.conn.cursor()
        self.conn.select_db('python')
        items = []
        sql ="select * from task_list"
        self.cur.execute(sql)
        result=self.cur.fetchall()
        for item in result:
            print item[2]
            yield Request(url=item[2]+"/search.htm", method='get', callback=self.parse_item)
        #url ="http://huantingsm.tmall.com/search.htm"
        #return [Request(url=url, method='get', callback=self.parse_item)]

    #抓取商品列表
    def parse_item(self,response):
        items = []
        html = response.body
        #rule = re.compile(r"detail.tmall.com/item.htm\?id=(\d+)&\" class=\"permalink\" style=\"\">\n+(.*)\n+</a>")
        item_list = self.r_pro_list_item.findall(html)  #匹配商品名称、ID
        sell_count = self.r_pro_list_sell_count.findall(html) #匹配总销量
        #rule_page = re.compile(r"J_SearchAsync next\" href=\"(.*)\"")
        page = self.r_pro_list_page.findall(html) #匹配下一页
        if  item_list:
            for i in item_list:
                #过滤总销量为0的商品
                if sell_count.pop()!="0":
                    value = 'http://detail.tmall.com/item.htm?id='+i[0]
                    #sql ="select * from task where url=%s"
                    #result= self.cur.execute(sql,value)
                    #if not result:
                        #sql = "insert into task(url) values(%s)"
                        #self.cur.execute(sql,value)
                        #self.conn.commit()
                    item = Website()
                    item['url'] = 'http://detail.tmall.com/item.htm?id='+i[0]
                    item['title'] = i[1].strip()
                    items.append(item)
                    items.extend([self.make_requests_from_url(value).replace(callback=self.parse_product)])
        if page:
            #sql ="select * from task where url=%s"
            #result= self.cur.execute(sql,page[0])
            #if not result:
                #sql = "insert into task(url) values(%s)"
                #self.cur.execute(sql,page[0])
                #self.conn.commit()
            item = Website()
            item['url'] = page[0]
            item['title'] = 'new page'
            items.append(item)
            items.extend([self.make_requests_from_url(page[0]).replace(callback=self.parse_item)])
        return items

    #抓取商品
    def parse_product(self,response):
        print '++++++++++++++++++++++++++++++++parse_product start'
        headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5"}
        items=[]
        html = self.conv(response.body)
        sell_url =self.r_init_url.search(html).group(1)
        product_id = self.r_pro_id.findall(html)
        headers['Referer'] = 'http://detail.tmall.com/item.htm?id='+str(product_id)
        response, content = self.http.request(sell_url, 'GET',headers=headers)
        content = self.conv(content)
        sell_count = self.r_sell_count.search(content).group(1)
        ####写入数据库
        print "MMMMMMMMMMMMMM:-----"+sell_count
        #过滤月销量为0的商品
        if sell_count!="0":
            buyer_list = self.r_pro_buyer_list.search(html)
            if buyer_list:
                buyer_list = buyer_list.group(1)
                buyer_list = buyer_list.replace("mdskip.taobao.com/extension/dealRecords.htm","tbskip.taobao.com/json/show_buyer_list.htm")
                item = Website()
                item['url'] = buyer_list
                item['title'] = 'buyer_list page'
                items.append(item)
                items.extend([self.make_requests_from_url(buyer_list).replace(callback=self.parse_buyer_list)])
        product_name = self.r_pro_name.findall(html)
        price = self.r_pro_price.findall(html)
        if price:
            print price

        ##写入商品的名称、价格
        if product_id and product_name:
            value = []
            value.append(product_id[0])
            value.append(product_name[0])
            value.append(price[0])
            sql = "insert into product(product_id,name,price) values(%s,%s,%s)"
            self.cur.execute(sql,value)
            self.conn.commit()
        print '++++++++++++++++++++++++++++++++parse_product end'
        return items


    #抓取商品成交记录
    def parse_buyer_list(self, response):
        print '++++++++++++++++++++++++++++++++parse_detail start'
        items = []
        html = self.conv(response.body)
        #当前页
        cur_page =int(self.r_buyer_cur_page.search(html).group(1))
        number = self.r_buyer_number.findall(html)
        number = [ int(i) for i in number]
        price = self.r_buyer_price.findall(html)
        price =[ int(i) for i in price]
        #time = rule5.findall(html)
        product_id = self.r_buyer_id.search(html).group(1)
        next_page =self.r_buyer_page.search(html)
        price_filter = [price[i] for i in range(len(price)) if price[i] not in price[:i]]
        result = {}
        for money in price_filter:
            result[money]= 0
            index =0
            for num in price:
                if num==money:
                    result[money] += number[index]
        ###result写入数据库
        #
        #
        #保存数据
        value = []
        count_money = 0
        count_num = 0
        for i in number:
            if price:
                count_money+=i*price.pop()
            count_num+=i
        #sql ="select money,count from detail where product_id=%s"
        #result= self.cur.execute(sql,product_id)
        #if result:
        #row = self.cur.fetchall()
        #count_money +=int(row[0][0])
        #count_num+=int(row[0][1])
            #self.cur.execute("delete from detail where product_id=%s",product_id)
            #self.conn.commit()
        value.append(product_id)
        value.append(count_money)
        value.append(count_num)
        sql = "insert into detail(product_id,money,count) values(%s,%s,%s)"
        self.cur.execute(sql,value)
        self.conn.commit()
        if cur_page > 2:
            return []
        #如果存在下一页
        if 1==2 and next_page:
            page_url = next_page.group(1).replace("amp;","")  #下一页的url
            #如果列表中还有未抓取的成交记录页面
            if self.page_list:
                    page_num = self.page_list.pop()
                    page_url = page_url.replace("bidPage="+str(cur_page),"bidPage="+str(page_num))
            #page_url = page_url.replace("mdskip.taobao.com/extension/dealRecords.htm","tbskip.taobao.com/json/show_buyer_list.htm")
            sql ="select * from task where url=%s"
            result= self.cur.execute(sql,page_url)
            if not result:
                sql = "insert into task(url) values(%s)"
                self.cur.execute(sql,page_url)
                self.conn.commit()
                item = Website()
                item['url'] = page_url
                item['title'] = 'buyer_list page'
                items.append(item)
                items.extend([self.make_requests_from_url(page_url).replace(callback=self.parse_buyer_list)])
                headers = {'Referer':''}
                headers['Referer'] = 'http://detail.tmall.com/item.htm?id='+str(product_id)
                return [Request(url=page_url, method='get',headers=headers ,callback=self.parse_buyer_list)]
        return items

    def conv(self,str):
        return str.decode('gbk')
        code =  chardet.detect(str)['encoding'].lower()
        if code =='utf-8':
            str = str.decode('utf-8')
        else:
            str = str.decode('gbk')
        return str