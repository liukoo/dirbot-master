# -*- coding: utf-8 -*-
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy import log
from scrapy.mail import MailSender

class SpiderOpenCloseLogging(object):

    def __init__(self):
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)
        self.mailer = MailSender()
        self.mailer.smtphost = "smtp.qq.com"
        self.mailer.smtpuser = "admin@liuko.com"
        self.mailer.smtppass = "5824205858"
        self.mailer.mailfrom = "admin@liuko.com"

    def spider_opened(self, spider):
        spider.conn.commit()
        log.msg("opened spider %s" % spider.name)
        if spider.domain:
            self.mailer.send(to=["lqf800@qq.com"], subject="scrapy", body="scrapy start:"+str(spider.domain))

    def spider_closed(self, spider):
        if spider.domain:
            param =(spider.sales_num,spider.money,spider.queue_id)
            spider.cur.execute("update queue set sales=%s , money=%s where id=%s",param)
            spider.conn.commit()
            spider.cur.close()
            spider.conn.close()
            self.mailer.send(to=[spider.mailto], subject="数据抓取结果", body="30天销量:"+str(spider.sales_num)+" \n30天成交额:"+str(spider.money)+"\n店铺地址:"+str(spider.domain))
        log.msg("closed spider %s" % spider.name)

