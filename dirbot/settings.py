#coding:utf-8
# Scrapy settings for dirbot project
SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Product'
ITEM_PIPELINES = ['dirbot.pipelines.FilterWordsPipeline']
DOWNLOADER_MIDDLEWARES = {
    #'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    #'dirbot.proxy.ProxyMiddleware': 100,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'dirbot.downloadmiddleware.rotate_useragent.RotateUserAgentMiddleware':400,
    }
EXTENSIONS = {
    'dirbot.include.signals.SpiderOpenCloseLogging':500,
}
#DOWNLOAD_DELAY = 1
DNSCACHE_ENABLED = True
DOWNLOAD_TIMEOUT = 20
CONCURRENT_REQUESTS = 50
COOKIES_ENABLED = False
#LOG_ENABLED = True
#LOG_ENCODING = 'utf-8'
#LOG_FILE = 'log.log'
#LOG_LEVEL = 'DEBUG'
#LOG_STDOUT = True
#AUTOTHROTTLE_ENABLED = True
#AUTOTHROTTLE_START_DELAY = 1
#AUTOTHROTTLE_CONCURRENCY_CHECK_PERIOD = 10
#CONCURRENT_REQUESTS_PER_SPIDER = 30
DB_INFO = {
    "HOST":'localhost',
    "USER":'root',
    "PASS":'',
    "PORT":3306
}
MAIL_HOST ='smtp.sina.cn'
MAIL_FROM='liuqingfei001@sina.cn'
MAIL_USER='liuqingfei001@sina.cn'
MAIL_PASS ='liuqingfei001'
MAIL_ADMIN = "lqf800@qq.com"