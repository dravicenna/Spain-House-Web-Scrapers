import re
import scrapy
from myparcer.items import MyparcerItem
#сколько страниц парсить
NUM_PAGE = 2

class my_spider(scrapy.Spider):
    name = "my_spider"
    # main_url = 'https://www.fotocasa.es/es/comprar/viviendas/espana/todas-las-zonas/l/'
    start_urls = ['https://www.fotocasa.es/es/comprar/viviendas/espana/todas-las-zonas/l/']

    def parse(self, response):
        u = 'https://www.fotocasa.es'
        #получаем ссылку на следующую страницу и ее номер
        myurl = u + response.xpath('//a[@class="sui-LinkBasic sui-PaginationBasic-link"]/@href').extract()[-1]
        page_namber = int(myurl.split('/')[-1])
        if page_namber <= NUM_PAGE:
            #все URL на объекты
            java_urls = re.findall(r'"detail":{"es-ES":"(.+?)("},"features")', response.body.decode("utf-8"))

            # for i in range(len(java_urls)): #выставляем количество объяектов для парса со страницы
            for i in range(2):
                link = u + java_urls[i][0]#.split('?')[0]
                yield response.follow(link, callback=self.parce_page, meta={'dont_redirect': True, 'handle_httpstatus_list': [302]})

            yield response.follow(myurl, callback=self.parse)

    def parce_page(self, response):

        self.logger.info('PARSING_PAGE %s', response.url)
        #распарсить строку с экстрапараметрами
        # featuresValues = re.findall(r'featuresValues = (.+?);', response.body.decode("utf-8"))
        alldata = re.findall(r'__INITIAL_PROPS__={"(.+?)"},{"name":', response.body.decode("utf-8"))
        # utag_data = re.findall(r'featuresValues = (.+?);', response.body.decode("utf-8"))

        #распарстить javascript с основными данными
        pure_java_text = response.xpath('//script[@type="text/javascript"]').getall()[2].replace('\r\n            ', ' ')
        house_data = pure_java_text[pure_java_text.find('utag_data ='):pure_java_text.find('};')].strip().split('=')[1]
        house_data = house_data.split('", ')

        #находим и сохраняем ссылки на картинки
        images = str(response.xpath('//input[@id="hidUrlsPhotos"]/@value').extract())
        images = images.split("|")
        for i in range(len(images)):
            images[i] = images[i].rsplit('/', 2)[0]

        #найдем телефон
        phone = str(response.xpath('//input[@id="hid_AdPhone"]/@value').extract()[0].split(':')[-1])

        #парсим этаж
        planta_test = response.xpath('//span[@id="litFloor"]/text()').extract()
        if planta_test:
            planta = response.xpath('//span[@id="litFloor"]/text()').extract()
        else:
            planta = 'NaN'

        #парсим описание detail-description
        full_description_test = response.xpath('//p[@class="detail-description"]/text()').extract()
        if full_description_test:
            # full_description = response.xpath('//p[@class="detail-description"]/text()').extract()[0].strip().rstrip('\r').rstrip('\n')
            full_description = response.xpath('//p[@class="detail-description"]/text()').extract()[0]
            full_description = re.sub("^\s+|\n|\r|\s+$", '', full_description)
        else:
            full_description = 'NaN'

        #пустой словарь и запись в него основных параметров
        data = {}
        # data = IdealistaparserItem()
        data['phone'] = phone
        data['featuresValues'] = featuresValues
        data['planta'] = planta
        for i in range(len(house_data)):
            key = house_data[i].split(': ')[0].replace('{', '').strip()
            value = house_data[i].split(': ')[1]
            value = value.replace('"', '')
            data[key] = value

        # здесь указываем сохранять или нет фотки
        # data['image_urls'] = images

        data['full_description'] = full_description
        data['url'] = response.url

        # session_path = str(response.url).split('/')[-1]
        # data['session_path'] = session_path
        yield data
