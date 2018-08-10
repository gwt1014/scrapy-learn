# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JingdongItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    comment_count = scrapy.Field()
    goods_url = scrapy.Field()
    goods_id = scrapy.Field()
    price = scrapy.Field()
    itemDetail = scrapy.Field()
    goodRate = scrapy.Field()
    commentCount = scrapy.Field()

class JDcommentItem(scrapy.Item):
    

    #用户名
    nickname = scrapy.Field()
    #商品链接
    goods_url = scrapy.Field()
    #商品id
    goods_id = scrapy.Field()
    #商品类型
    productColor = scrapy.Field()
    #评分
    score = scrapy.Field()
    # 评论
    content = scrapy.Field()
    #评论时间
    creationTime = scrapy.Field()
    #追评
    afterUserComment = scrapy.Field()
    #追评时间
    afterDays = scrapy.Field()


