# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZiruItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    houseID = scrapy.Field()
    name = scrapy.Field()
    houseType = scrapy.Field()
    district = scrapy.Field()
    region = scrapy.Field()
    area = scrapy.Field()
    direction = scrapy.Field()
    house_type = scrapy.Field()
    price = scrapy.Field()
    price_type = scrapy.Field()
    floor = scrapy.Field()
    subway1 = scrapy.Field()
    subway2 = scrapy.Field()
    subway3 = scrapy.Field()
    subway_station1 = scrapy.Field()
    subway_distance1 = scrapy.Field()
    subway_station2 = scrapy.Field()
    subway_distance2 = scrapy.Field()
    subway_station3 = scrapy.Field()
    subway_distance3 = scrapy.Field()
    subway_station4 = scrapy.Field()
    subway_distance4 = scrapy.Field()
    traffic = scrapy.Field()
    around = scrapy.Field()
    housing_allocation = scrapy.Field()
    room_tag = scrapy.Field()
    house_url = scrapy.Field()
