#coding:utf-8
from scrapy.item import Item, Field
class Product(Item):
    product_id = Field() #商品ID
    shop_id = Field()    #商店ID
    price  = Field()     #价格
    sales = Field()      #月销量
    name = Field()       #商品标题
    url = Field()        #商品链接
