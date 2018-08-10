# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class TaobaoPipeline(object):
    # def process_item(self, item, spider):
    #     title = item['title']
    #     link = item['itemLink']
    #     price = item['price']
    #     itemID = item['itemID']
    #     # salesVolume = item['salesVolume']
    #     # comment = item['comment']
    #     itemInfo = item['itemInfo']
    #     print('商品名字', title)
    #     print('商品链接', link)
    #     print('商品ID', itemID)
    #     print('商品价格', price)
    #     # print('商品销量', salesVolume)
    #     # print('商品评论数量', comment)
    #     print('商品详情', itemInfo)
    #     print('------------------------------\n')
    #     return item

    def __init__(self):
        self.f = open("taobao.json" , "wb")

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii = False) + ", \n"
        self.f.write(content.encode("utf-8"))
        return item

    def close_spider(self , spider):
        self.f.close()