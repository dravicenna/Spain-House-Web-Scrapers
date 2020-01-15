# -*- coding: utf-8 -*-
import re
import scrapy
from myparcer.items import MyparcerItem


# scrapy crawl foto_venda
# scrapy crawl foto_venda -s LOG_FILE=foto_venda.log
# scrapy crawl foto_venda -s LOG_FILE=foto_venda.log -a tag=lloret
# scrapy parse --spider=foto_venda -d 2 -v https://www.fotocasa.es/es/comprar/viviendas/espana/todas-las-zonas/l/
# scrapy shell -s USER_AGENT="Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7" https://www.fotocasa.es/vivienda/valencia-capital/valencia-ciudad-jardin-terraza-ascensor-calle-eduardo-soler-y-perez-10-149317148
# scrapy crawl foto_venda -s JOBDIR=crawls/foto_venda-1


#сколько страниц парсить
# NUM_PAGE = 2

class FotoVendaSpider(scrapy.Spider):
    name = 'foto_venda'
    # allowed_domains = ['www.fotocasa.es/es/comprar/viviendas/espana/todas-las-zonas/l/']
    start_urls = ['https://www.fotocasa.es/es/comprar/viviendas/espana/todas-las-zonas/l/']
    custom_settings = {
        'DEPTH_LIMIT': 1,
        'FEED_URI': 'csv/fotovenda.csv'
    }

    def parse(self, response):
        u = 'https://www.fotocasa.es'
        url_for_casas = 'https://www.fotocasa.es/es/comprar'
        # получаем ссылку на следующую страницу и ее номер
        next_page_url = u + response.xpath('//a[@class="sui-LinkBasic sui-PaginationBasic-link"]/@href').extract()[-1]

        print('NEXT >>>> ', next_page_url)
        # page_namber = int(next_page_url.split('/')[-1])

        # все URL на объекты
        java_urls = re.findall(r'"detail":{"es-ES":"(.+?)"},"features"', response.body.decode("utf-8"))
        # for i in range(len(java_urls)): #выставляем количество объяектов для парса со страницы
        for i in range(2):
            link = u + java_urls[i]#.split('?')[0] + '/d'
            print("LINK>>>>>>>>  ", link)
            yield response.follow(link, callback=self.parce_page)#, meta={'dont_redirect': True, 'handle_httpstatus_list': [302]})

        yield response.follow(next_page_url, callback=self.parse)



    def parce_page(self, response):
        data = MyparcerItem()
        # распарсить строку с параметрами
        raw_data = re.findall(r'__INITIAL_PROPS__={"(.+?)"},{"name":', response.body.decode("utf-8"))
        data['raw_data'] = raw_data
        yield data

