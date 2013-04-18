from scrapy.exceptions import DropItem
from scrapy.http import Request
class FilterWordsPipeline(object):
    def process_item(self, item, spider):
        print 'pipeline process_item-----------------run start'
        print item['title']
        print item['price']
        print item['sales']
        print 'pipeline process_item-----------------run end'
        return item