# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiazfItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # name = scrapy.Field()
    houseID = scrapy.Field()  # ID
    title = scrapy.Field()  # 房屋名称
    district = scrapy.Field()  # 城区
    block = scrapy.Field()  # 地区
    communityName = scrapy.Field()  # 小区名称
    houseLink = scrapy.Field()  # 房屋链接

    roommainInfo = scrapy.Field()  # 房屋户型
    floor = scrapy.Field()  # 所在楼层
    orientation = scrapy.Field()  # 房屋朝向
    builtArea = scrapy.Field()  # 建筑面积

    subway = scrapy.Field()  # 地铁
    heatingMode = scrapy.Field()  # 供暖方式
    houseState = scrapy.Field()  # 房屋现状
