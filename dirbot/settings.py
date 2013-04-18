# Scrapy settings for dirbot project
SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Product'
ITEM_PIPELINES = ['dirbot.pipelines.FilterWordsPipeline']
DOWNLOAD_DELAY = 1.6
DNSCACHE_ENABLED = True
DOWNLOAD_TIMEOUT = 30