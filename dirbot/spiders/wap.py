# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
import re,MySQLdb,httplib2
from dirbot.items import Product
from dirbot.tools import conv
class DmozSpider(CrawlSpider):
    name = "wap"
    allowed_domains = ["tmall.com","taobao.com"]
    def __init__(self):
        ####################################################################################################################
        self.Shop = re.compile(r"shopId=(\d*);")
        self.p_url = re.compile(r"<a href=\"http://a\.m\..*/i(.*)\.htm") #匹配商品链接
        self.item_list = re.compile(ur"data-url=\"(.*)\u6240\u6709\u5b9d")  #匹配所有宝贝链接
        self.price1 = re.compile(r"\"promoPrice\":\"(\d*\.\d*)")  #促销价
        self.price2 = re.compile(r"\"price\":\"(\d*\.\d*)")   #原价
        self.price3 = re.compile(r"price: \".(\d*\.\d*)\"")
        self.sales  = re.compile(ur"(\d*) \u4ef6")  #匹配销量
        self.pid = re.compile(r"\"item_id\" value=\"(\d*)\"")  #匹配商品ID
        self.b_shopid = re.compile(r"shop_id=(\d*)&amp")  #商城店铺ID
        self.c_shopid = re.compile(r"shop(\d*)\.m")      #C店店铺ID
        self.d_shopid = re.compile(r"shop(\d*)\.m")      #C店店铺ID
        self.next_page = re.compile(r"c-pnav-next\">\r\n<a href=\"(.*)\"") #下一页
        ####################################################################################################################
        self.http =httplib2.Http()
        self.conn=MySQLdb.connect(host='localhost',user='root',passwd='',port=3306,charset='utf8')
        self.cur=self.conn.cursor()
        self.conn.select_db('python')
        self.amount_num = 0
        self.amount_money = 0
        self.domain = "http://delixiguojidiangong.tmall.com/"

    #开始
    def start_requests(self):
        yield Request(self.domain, method='get', callback=self.parse_shop)

    #开始抓取店铺
    def parse_shop(self,response):
        items = []
        html = conv(response.body)
        wap = self.Shop.search(html).group(1)
        wap = "http://shop"+wap+".m.taobao.com/"
        web = httplib2.Http()
        r,c = web.request(wap, 'GET',headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31"})
        c = conv(c)
        all_link = self.item_list.search(c).group(1).replace("&amp;",'&')
        yield Request(all_link, method='get', callback=self.parse_item)

    #抓取商品列表
    def parse_item(self,response):
        items = []
        html = conv(response.body)
        product_list = self.p_url.findall(html)
        next_page =self.next_page.search(html)
        if product_list:
            for link in product_list:
                url = "http://a.m.taobao.com/i"+link+".htm"
                items.extend([self.make_requests_from_url(url).replace(callback=self.parse_product)])
        if next_page:
           page_url = next_page.group(1).replace("&amp;",'&')
           items.extend([self.make_requests_from_url(page_url).replace(callback=self.parse_item)])
        return items

    #抓取商品
    def parse_product(self,response):
        print '++++++++++++++++++++++++++++++++parse_product start'
        items=[]
        html = conv(response.body)
        price = self.price1.search(html)#促销价
        if price:
            price = price.group(1)
        else:
            price = self.price2.search(html)
            if price:
                price = price.group(1)
            else:
                price = self.price3.search(html).group(1)

        sales = self.sales.search(html).group(1)  #月销量
        shopid = self.b_shopid.search(html)  #匹配商城的店铺ID
        if shopid:
            shopid = shopid.group(1)
        else:
            shopid = self.c_shopid.search(html).group(1)

        pid = self.pid.search(html).group(1)

        print "MMMMMMMMMMMMMM:-----"+sales
        #过滤月销量为0的商品
        if int(sales)>0:
            self.amount_num+=int(sales)
            self.amount_money+=float(sales)*float(price)
            item = Product()
            item['shop_id'] = shopid
            item['sales'] = sales
            item['price']= price
            item['url']= "http://m.taobao.com/i"+pid+".htm"
            item['name'] = ""
            item['product_id'] =pid
            items.append(item)
        print '++++++++++++++++++++++++++++++++parse_product end'
        print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        print self.domain
        print "num:"+str(self.amount_num)
        print "money"+str(self.amount_money)
        print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        return items
