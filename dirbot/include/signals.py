# -*- coding: utf-8 -*-
#Last Modify 2013.5.9  10:38
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy import log
from dirbot.include.tools import sendMail
from dirbot.settings import MAIL_ADMIN
from dirbot.settings import DEBUG
import datetime
import httplib2
from urllib import urlencode
class SpiderOpenCloseLogging(object):
    def __init__(self):
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_opened(self, spider):
        log.msg("opened spider %s" % spider.name)
        if not DEBUG:
            sendMail(MAIL_ADMIN,'scrapy running','scrapy is start')

    def spider_closed(self, spider):
        http = httplib2.Http()
        if spider.type ==1:
            param =(spider.task_id,spider.store_id,spider.sales_num,spider.money,datetime.date.today())
            spider.cur.execute("insert into store_info(task_id,store_id,sale_count,sale_money,date) values(%s,%s,%s,%s,%s)",param)
            spider.conn.commit()
            if spider.check_task():
                data={'project':"dirbot","spider":"cron"}
                header={'Content-Type': 'application/x-www-form-urlencoded'}
                s,c = http.request("http://localhost:6800/schedule.json","POST",urlencode(data),headers=header)

        if spider.type==2 and spider.domain:
            spider.domain = 'http://'+spider.domain
            param =(spider.sales_num,spider.money,spider.queue_id)
            spider.cur.execute("update queue set sales=%s , money=%s where id=%s",param)
            spider.conn.commit()
            mail_content = str(spider.shop_name)+"\n"
            mail_content += "30天销量:"+str(spider.sales_num)+"\n "+"30天成交额:"+str(spider.money)+"\n"+"店铺地址:"+str(spider.domain)+"\n"
            mail_content+="---------------------------------------\n"
            mail_content+=spider.shopinfo_str
            mail_title = str(spider.shop_name) +' 数据报告'
            mail_title = mail_title.decode('utf-8')
            sendMail(spider.mailto,mail_title,mail_content)
        spider.cur.close()
        spider.conn.close()
        log.msg("closed spider %s" % spider.name)