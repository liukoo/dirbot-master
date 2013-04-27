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
        self.mailer.smtphost = "smtp.sina.cn"
        self.mailer.smtpuser = "liuqingfei001@sina.cn"
        self.mailer.smtppass = "liuqingfei001"
        self.mailer.mailfrom = "liuqingfei001@sina.cn"

    def spider_opened(self, spider):
        log.msg("opened spider %s" % spider.name)
        self.mailer.send(to=["lqf800@qq.com"], subject="scrapy running", body="scrapy is start")

    def spider_closed(self, spider):
        if spider.domain:
            param =(spider.sales_num,spider.money,spider.queue_id)
            spider.cur.execute("update admin_queue set sales=%s , money=%s where id=%s",param)
            spider.conn.commit()
            spider.cur.close()
            spider.conn.close()
            mail_content = str(spider.shop_name)+"\n"
            mail_content += "30天销量:"+str(spider.sales_num)+" \n30天成交额:"+str(spider.money)+"\n店铺地址:"+str(spider.domain)+"\n"
            mail_title = str(spider.shop_name) +' 数据报告'
            self.mailer.send(to=[str(spider.mailto)], subject=mail_title, body=mail_content)
        log.msg("closed spider %s" % spider.name)

