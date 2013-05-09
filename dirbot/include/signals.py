# -*- coding: utf-8 -*-
#Last Modify 2013.5.9  10:38
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy import log
from dirbot.include.tools import sendMail
from dirbot.settings import MAIL_ADMIN
class SpiderOpenCloseLogging(object):
    def __init__(self):
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_opened(self, spider):
        log.msg("opened spider %s" % spider.name)
        sendMail(MAIL_ADMIN,'scrapy running','scrapy is start')

    def spider_closed(self, spider):
        if spider.domain:
            spider.domain = 'http://'+spider.domain
            param =(spider.sales_num,spider.money,spider.queue_id)
            spider.cur.execute("update admin_queue set sales=%s , money=%s where id=%s",param)
            spider.conn.commit()
            spider.cur.close()
            spider.conn.close()
            mail_content = str(spider.shop_name)+"\n"
            mail_content += "30天销量:"+str(spider.sales_num)+"\n "+"30天成交额:"+str(spider.money)+"\n"+"店铺地址:"+str(spider.domain)+"\n"
            mail_content+="---------------------------------------\n"
            mail_content+=spider.shopinfo_str
            mail_title = str(spider.shop_name) +' 数据报告'
            mail_title = mail_title.decode('utf-8')
            sendMail(spider.mailto,mail_title,mail_content)
        log.msg("closed spider %s" % spider.name)