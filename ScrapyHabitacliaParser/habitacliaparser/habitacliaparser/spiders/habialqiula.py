# -*- coding: utf-8 -*-
import scrapy


class HabialqiulaSpider(scrapy.Spider):
    name = 'habialqiula'
    allowed_domains = ['https://www.habitaclia.com/alquiler-abrera.htm']
    start_urls = ['https://www.habitaclia.com/alquiler-abrera.htm/']

    def parse(self, response):
        pass
