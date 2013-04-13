from scrapy.exceptions import DropItem
from scrapy.http import Request
import chardet
class FilterWordsPipeline(object):
    def process_item(self, item, spider):
        print 'pipeline process_item-----------------run start'
        code =  chardet.detect(item['title'])['encoding'].lower()
        if code =='utf-8':
            title = item['title'].decode('utf-8')
        else:
            title = item['title'].decode('gbk')
        print title
        print 'pipeline process_item-----------------run end'
        return item