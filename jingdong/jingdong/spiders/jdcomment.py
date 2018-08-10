# -*- coding: utf-8 -*-
import scrapy
import json
from jingdong.items import JDcommentItem
import re


class JdcommentSpider(scrapy.Spider):
    name = 'jdcomment'

    def start_requests(self):
        init_search = 'https://coll.jd.com/list.html?sub=23931&sort=sort_totalsales15_desc&stock=0&page='
        # init_search = 'https://list.jd.com/list.html?cat=9192,9197,12189&page='
        # target = {'行车记录仪': '23931'}  sub后面的代号
        maxpage = 1
        for i in range(1, maxpage + 1):
            yield scrapy.Request(url=init_search + str(i), callback=self.getitemList)
            # print(init_search+str(i))
            # print("#"*40)

    def getitemList(self, response):

        itemList = response.xpath(
            '//div[@id="plist"]/ul/li/div/div[@class="p-name"]/a/@href').extract()
        for itemUrl in itemList:
            # print('https:'+ itemUrl)
            yield scrapy.Request(url=('https:' + itemUrl), callback=self.getitemIdlist)

    def getitemIdlist(self, response):
        item = JDcommentItem()
        init_itemUrl = 'https://item.jd.com/{}.html'
        init_commentUrl = 'https://sclub.jd.com/comment/productPageComments.action?productId={}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
        itemList = response.xpath(
            '//div[@id="choose-attrs"]/div//div[@class="dd"]/div/@data-sku').extract()
        for itemid in itemList:
            # print(init_itemUrl.format(itemid))
            item['goods_id'] = itemid
            item['goods_url'] = init_itemUrl.format(itemid)
            yield scrapy.Request(url=init_commentUrl.format(itemid), meta={'item': item}, callback=self.getitemComment)
            
####评论没做翻页！！！

    def getitemComment(self, response):

        item = response.meta['item']
        try:
            jc = json.loads(response.text)
            commentlist = jc['comments']
            for comment in commentlist:

                item['nickname'] = comment['nickname']

                item['productColor'] = comment['productColor']

                item['score'] = comment['score']

                item['content'] = comment['content']

                item['creationTime'] = comment['creationTime']

                if 'afterUserComment' in comment:

                    item['afterUserComment'] = comment['afterUserComment']['hAfterUserComment']['content']

                    item['afterDays'] = comment['afterUserComment']['created']

                else :
                    item['afterUserComment'] = None
                    
                    item['afterDays'] = None

                yield item

        except Exception as e:
            print('没有评论数据')

