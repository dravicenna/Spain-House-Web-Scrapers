# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IdealistaparserItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    title_minor = scrapy.Field()
    txt_diposit = scrapy.Field()
    price = scrapy.Field()
    ft = scrapy.Field()
    tel = scrapy.Field()
    URL = scrapy.Field()
    describe = scrapy.Field()
    detail_1 = scrapy.Field()
    detail_2 = scrapy.Field()
    adress = scrapy.Field()
    stat_text = scrapy.Field()
    vender_type = scrapy.Field()
    vender_name = scrapy.Field()
    image_urls = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()

