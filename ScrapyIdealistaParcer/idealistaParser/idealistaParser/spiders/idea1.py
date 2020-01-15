# -*- coding: utf-8 -*-
import scrapy
from idealistaParser.items import IdealistaparserItem
import  re
# scrapy shell -s USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36" https://www.idealista.com/inmueble/84402140/
class Idea1Spider(scrapy.Spider):
    name = 'idea1'
    # allowed_domains = ['https://www.idealista.com']
    # start_urls = ['https://www.idealista.com/login']
    start_urls = ['https://www.idealista.com/alquiler-viviendas/lloret-de-mar-girona/']

    def parse(self, response):
        main_url = 'https://www.idealista.com'

        urls = response.xpath('//a[@class="item-link "]/@href').extract()
        # checking next link exist
        print('COUNT: >>>>>>>', len(urls))

        for i in range(len(urls)):
        # for i in range(2):
            yield response.follow(main_url + urls[i], callback=self.parse_page)

        next_link = response.xpath('//li[@class="next"]/a[@class="icon-arrow-right-after"]/@href').extract_first()
        if next_link:
            next_link = main_url + str(next_link)
            yield response.follow(next_link, callback=self.parse)

    def parse_page(self, response):
        print('PARSE PAGE HERE')
        # create dictionary for data
        scraped_info = IdealistaparserItem()
        scraped_info['title'] = response.xpath('//span[@class="main-info__title-main"]/text()').extract()
        scraped_info['title_minor'] = response.xpath('//span[@class="main-info__title-minor"]/text()').extract()
        scraped_info['txt_diposit'] = response.xpath('//span[@class="txt-deposit"]/span/text()').extract()
        scraped_info['price'] = response.xpath('//span[@class="info-data-price"]/span/text()').extract_first().replace('.', '')

        scraped_info['describe'] = response.xpath('//div[@class="adCommentsLanguage expandable"]/text()').extract()
        scraped_info['detail_1'] = response.xpath('//*[@id="details"]/div/div[1]/div/ul/li/text()').extract()
        scraped_info['detail_2'] = response.xpath('//*[@id="details"]/div/div[2]/div/ul/li/text()').extract()
        scraped_info['adress'] = response.xpath('//*[@id="headerMap"]/ul/li/text()').extract()
        scraped_info['stat_text'] = response.xpath('//*[@id="stats"]/p/text()').get()
        scraped_info['stat_text'] = response.xpath('//*[@id="stats"]/p/text()').get()
        scraped_info['vender_type'] = response.xpath('//div[@class="professional-name"]/div/text()').get().strip()
        scraped_info['vender_name'] = response.xpath('//div[@class="professional-name"]/span/text()').get().strip()
        #
        scraped_info['img_urls'] = re.findall(r'https:\/\/img3\..+?jpg', response.body.decode("utf-8"))[1:]
        tel = response.xpath('//span[@class="phone-btn-number"]/text()').extract_first()
        if tel:
            tel = tel.strip(' ')
        scraped_info['tel'] = tel
        info_features_list = response.xpath('//div[@class="info-features"]/span').extract()
        for i in range(len(info_features_list)):
            info_features_list[i] = info_features_list[i].replace('<span>', '').replace('</span>', '').strip()
        # print(info_features_list)
        scraped_info['ft'] = info_features_list
        yield scraped_info
