# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

# 名称
    title = scrapy.Field()
# 价格
    price = scrapy.Field()
# 月销量
    # salesVolume = scrapy.Field()
# # 评论数
#     comment = scrapy.Field()
# 宝贝详情
    itemInfo = scrapy.Field()
# 链接
    itemLink = scrapy.Field()
# 宝贝ID
    itemID = scrapy.Field()
# # 评论？这个多条可以考虑爬取两次然后merge

