# -*- coding: utf-8 -*-
import scrapy
from idealistaParser.items import IdealistaparserItem
import re
# import datetime

# scrapy crawl idea_vend -s LOG_FILE=idea_vend.log -a tag=lloret
# scrapy crawl idea_vend -s JOBDIR=crawls/idea_vend-1
# https://www.idealista.com/buscar/venta-terrenos/lloret/

class IdeaVendSpider(scrapy.Spider):
    name = 'idea_vend'
    # allowed_domains = ['https://www.fotocasa.es/es/alquiler/viviendas/lloret-de-mar/todas-las-zonas/l']
    start_urls = ['https://www.idealista.com/buscar/venta-viviendas/lloret-de-mar-girona/lloret/']

    # set custom settings
    custom_settings = {
        # 'DEPTH_LIMIT': 3,
        'FEED_URI': 'scraped_data/idealista_venda_april.csv',
        'IMAGES_STORE': 'scraped_data/images/'
    }

    def __init__(self, *args, **kwargs):
        super(IdeaVendSpider, self).__init__(*args, **kwargs)


    def start_requests(self):
        tag = getattr(self, 'tag', None)
        url = 'https://www.idealista.com/buscar/venta-viviendas/{}/'
        if tag is not None:
            url = url.format(tag)
        else:
            url = self.start_urls[0]
        yield scrapy.Request(url, self.folow_correct_link)


    def folow_correct_link(self, response):
        main_url = 'https://www.idealista.com'
        url = main_url + response.xpath('//*[@id="facets-list"]/ul[1]/li[1]/a/@href').extract_first()
        yield scrapy.Request(url, self.parse)


    def parse(self, response):
        main_url = 'https://www.idealista.com'
        urls = response.xpath('//a[@class="item-link "]/@href').extract()
        tag = getattr(self, 'tag', None)
        if len(urls) == 0:
            print('Can\'t find anything. CHECK ARGUMENT: {}'.format(tag))

        for i in range(len(urls)):
        # for i in range(2):
            yield response.follow(main_url + urls[i], callback=self.parse_page)

        next_link = response.xpath('//li[@class="next"]/a[@class="icon-arrow-right-after"]/@href').extract_first()
        # checking next link exist
        if next_link:
            next_link = main_url + str(next_link)
            yield response.follow(next_link, callback=self.parse, meta={'dont_redirect': True, 'handle_httpstatus_list': [302]})


    def parse_page(self, response):
        print('PARSE PAGE HERE')
        # create dictionary for data
        scraped_info = IdealistaparserItem()
        scraped_info['URL'] = response.url.split('?')[0]
        scraped_info['title'] = response.xpath('//span[@class="main-info__title-main"]/text()').extract()
        scraped_info['title_minor'] = response.xpath('//span[@class="main-info__title-minor"]/text()').extract()
        # scraped_info['txt_diposit'] = response.xpath('//span[@class="txt-deposit"]/span/text()').extract()
        scraped_info['price'] = response.xpath('//span[@class="info-data-price"]/span/text()').extract_first().replace('.', '')
        scraped_info['describe'] = response.xpath('//div[@class="adCommentsLanguage expandable"]/text()').extract()
        scraped_info['detail_1'] = response.xpath('//*[@id="details"]/div/div[1]/div/ul/li/text()').extract()
        scraped_info['detail_2'] = response.xpath('//*[@id="details"]/div/div[2]/div/ul/li/text()').extract()
        scraped_info['adress'] = response.xpath('//*[@id="headerMap"]/ul/li/text()').extract()
        scraped_info['stat_text'] = response.xpath('//*[@id="stats"]/p/text()').get()
        scraped_info['stat_text'] = response.xpath('//*[@id="stats"]/p/text()').get()
        scraped_info['vender_type'] = response.xpath('//div[@class="professional-name"]/div/text()').get().strip()
        scraped_info['vender_name'] = response.xpath('//div[@class="professional-name"]/span/text()').get().strip()
        # for image downloading
        # scraped_info['image_urls'] = re.findall(r'https:\/\/img3\..+?jpg', response.body.decode("utf-8"))[1:]
        scraped_info['latitude'] = re.findall(r'latitude:\"(.+?\d)\"', response.body.decode("utf-8"))
        scraped_info['longitude'] = re.findall(r'longitude:\"(.+?\d)\"', response.body.decode("utf-8"))
        #try to get and clean telephone number
        try:
            tel = response.xpath('//span[@class="phone-btn-number"]/text()').extract_first().replace(' ', '')
        except:
            tel = []
        scraped_info['tel'] = tel
        #get features
        info_features_list = response.xpath('//div[@class="info-features"]/span').extract()
        for i in range(len(info_features_list)):
            info_features_list[i] = info_features_list[i].replace('<span>', '').replace('</span>', '').strip()
        scraped_info['ft'] = info_features_list
        yield scraped_info