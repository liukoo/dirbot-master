# Scrapy settings for dirbot project
SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Product'
ITEM_PIPELINES = ['dirbot.pipelines.FilterWordsPipeline']
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'dirbot.proxy.ProxyMiddleware': 100,
    }
DOWNLOAD_DELAY = 1
DNSCACHE_ENABLED = True
DOWNLOAD_TIMEOUT = 30
#LOG_ENABLED = True
#LOG_ENCODING = 'utf-8'
#LOG_FILE = 'sitemap.log'
#LOG_LEVEL = 'DEBUG'
#LOG_STDOUT = True