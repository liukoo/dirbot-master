# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re,time
import datetime
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
import MySQLdb
import httplib2
from dirbot.items import Product
from dirbot.include.tools import conv
from dirbot.settings import DB_INFO
class CronSpider(CrawlSpider):
    name = "cron"
    allowed_domains = ["tmall.com","taobao.com"]
    def __init__(self,**kwargs):
        super(CrawlSpider, self).__init__(self, **kwargs)
        self.http = httplib2.Http()
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
        self.shopname= re.compile(r"<title>(.*) -") #店铺名称
        self.product_title = re.compile(r"<title>.*-(.*)</title>")  #商品标题
        self.shop_info = re.compile(r"<label>(.*)</label>(\d\.\d)\r*\s*<em.*>(.*)</em>") #店铺评分
        ####################################################################################################################
        self.http =httplib2.Http()
        self.conn=MySQLdb.connect(host=DB_INFO['HOST'],user=DB_INFO['USER'],passwd=DB_INFO['PASS'],port=DB_INFO['PORT'],charset='utf8')
        self.cur=self.conn.cursor(MySQLdb.cursors.DictCursor)
        self.conn.select_db('python')
        self.sales_num = 0
        self.money = 0
        self.domain = 0
        self.mailto = 0
        self.queue_id = 0
        self.shop_name= 0
        self.shopinfo_str ="" #店铺评分信息
        ################################
        self.task_id =''
        self.store_id =''
        self.sale_count =''
        self.sale_money =''
        self.type =1
        ################################

    def __str__(self):
        return "Taobao-Cron-spider V0.2 Coding By:liukoo"
    #开始
    def start_requests(self):
        url = self.queue_pop() #从队列中读取一个店铺的url
        if url:
            url = 'http://'+url +'/'
            yield Request(url, method='get', callback=self.parse_shop)
        else:
            self.log("Queue is Empty!")
            self.log(self.domain)

    #开始抓取店铺
    def parse_shop(self,response):
        header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31"}
        items = []
        html = conv(response.body)
        wap = self.Shop.search(html).group(1)
        shop_info_url = "http://shop%s.m.taobao.com/shop/shop_info.htm?shop_id=%s" % (wap,wap)
        wap = "http://shop"+wap+".m.taobao.com/"
        web = self.http
        r,c = web.request(wap, 'GET',headers=header)
        html = conv(c)
        self.shop_name = self.shopname.search(html).group(1)
        all_link = self.item_list.search(html).group(1).replace("&amp;",'&')
        r,c = web.request(shop_info_url, 'GET',headers=header)
        html = conv(c)
        info = self.shop_info.findall(html)
        for item in info:
            self.shopinfo_str+=item[0] +":" +item[1] +item[2]+"\n"
        yield Request(all_link, method='get', callback=self.parse_item)

    #解析商品列表页
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

    #解析商品详情页
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
                try:
                 price = self.price3.search(html).group(1)
                except AttributeError:
                    return items
        #判断是不是运费补差商品,是的话不计入总销量
        flag = 0
        if float(price)==1.0 and self.product_title.search(html).group(1).find("补差")!=-1:
            flag =1
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
            if not flag:   #运费补差商品不计入总销量
                self.sales_num+=int(sales)
            self.money+=float(sales)*float(price)
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
        print "num:"+str(self.sales_num)
        print "money"+str(self.money)
        print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
        return items

    #检查今日是否还有要抓取的店铺
    def check_task(self):
        return True
        day =   datetime.date.today()
        day_s = day+datetime.timedelta(-1)
        day_s = time.strptime(str(day_s)+'-0:0:0','%Y-%m-%d-%H:%M:%S')
        day_s = time.mktime(day_s)
        sql ="select id from task  where task.stat='1' and last_time<%s limit 1" % day_s
        self.cur.execute(sql)
        return self.cur.rowcount
    #从队列中读取任务信息
    def queue_pop(self):
        now = int(time.time())
        day =   datetime.date.today()
        day_s = day+datetime.timedelta(-1)
        day_s = time.strptime(str(day_s)+'-0:0:0','%Y-%m-%d-%H:%M:%S')
        day_s = time.mktime(day_s)
        sql ="select * from task LEFT JOIN store on task.store_id=store.id  where task.stat='1' or last_time<%s limit 1" % day_s
        flag= self.cur.execute(sql)
        if flag:
            line = self.cur.fetchone()
            self.cur.execute("LOCK TABLES task WRITE")
            self.task_id = line['id']
            self.store_id = line['store_id']
            shop_url = line['store_url']
            self.cur.execute("update task set last_time=%s where id=%d" % (now,self.task_id))
            self.conn.commit()
            self.cur.execute("UNLOCK TABLES")
            self.domain = shop_url
            print shop_url
            return shop_url
        return False
