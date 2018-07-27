# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Lianjia2SfItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    houseID = scrapy.Field() #ID
    title = scrapy.Field() #房屋名称
    district = scrapy.Field() #城区
    block = scrapy.Field() #地区
    communityName = scrapy.Field() #小区名称
    totlePrice = scrapy.Field() #总价
    unitPrice = scrapy.Field() #单价
    houseLink = scrapy.Field()#房屋链接


    roommainInfo = scrapy.Field()# 房屋户型 
    floor = scrapy.Field() # 所在楼层
    builtArea = scrapy.Field() # 建筑面积
    roomType = scrapy.Field() # 户型结构（平层、跃层）
    useArea = scrapy.Field() # 套内面积
    builtType = scrapy.Field() # 建筑类型(塔楼、板楼)
    orientation = scrapy.Field() # 房屋朝向
    built = scrapy.Field() # 建筑结构（钢混）
    decoration = scrapy.Field() # 装修情况
    liftType = scrapy.Field() # 梯户比例
    heatingMode = scrapy.Field() # 供暖方式
    lift = scrapy.Field() # 配备电梯
    propertyRights = scrapy.Field() # 产权年限




    houseType = scrapy.Field() #房屋用途（普通住宅、别墅）