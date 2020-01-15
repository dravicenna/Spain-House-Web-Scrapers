import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import time
from geopy.geocoders import Nominatim

main_url = 'https://www.fotocasa.es/es/comprar/viviendas/espana/todas-las-zonas/l/{}'
# url_for_parce = 'https://www.fotocasa.es/vivienda/cordoba-capital/aire-acondicionado-terraza-fatima-levante-149567058?RowGrid=23&tti=1&opi=300'


def getPageLinks(page_number):
    page_link = main_url.format(page_number)
    r = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
    soup = BeautifulSoup(r.text, 'lxml')
    links = soup.findAll('a', attrs={'class': 're-Card-link'})
    first_link = 'https://www.fotocasa.es{}'
    links = [first_link.format(link.attrs['href']) for link in links]
    return links


def get_page_data(html):
    # готовим суп

    r = requests.get(html, headers={'User-Agent': UserAgent().chrome})
    print('Status connect: ' + str(r.status_code))
    soup = BeautifulSoup(r.text, 'lxml')

    # получаем тайтл страницы и ватыскиваем тип недвижимости
    title = soup.find('section', attrs={'class': 'section section--noBorder'}). \
        find('div', attrs={'class': 'detail-section-content'}).text.strip()

    type_of_house = title.split(' en ')[0].strip()

    #ищем адрес
    s = soup.find('span', id='ctl00_content1_PaginationTop_breadcrumbclassic_lbl_LocalizationUpperLevelwithLink')
    s = s.text
    s = s + ' Spain'
    geolocator = Nominatim(user_agent=UserAgent().chrome)
    location = geolocator.geocode(s)
    adress = title if not location else location.address

    #rooms
    habitaciones = soup.find('span', id='litRooms')
    habitaciones = "" if not habitaciones else habitaciones.text.strip().split(" ")[0]

    #Ванные комнаты
    bano = soup.find('span', id='litBaths')
    bano = "" if not bano else bano.text.strip().split(" ")[0]

    #Жилая Площадь
    surface_house = soup.find('span', id='litSurface')
    surface_house = "" if not surface_house else surface_house.text.strip().split(" ")[0]

    # Этаж
    planta = soup.find('span', id='litFloor')
    planta = "" if not planta else planta.text.strip()

    # цена
    price_house = soup.find('span', id='priceContainer').text.replace('.', '').split('€')[0].strip()

    # агенство
    agancy_name = soup.find('a', id='lnkMoreBuildings')
    agancy_name = "" if not agancy_name else agancy_name.text.strip()

    #номер телефона
    telefon = soup.find('input', attrs={'name': 'ctl00$hid_AdPhone'})
    telefon = "" if not telefon else telefon.attrs['value'].strip().split(':')[-1]

    # получаем список URL картинок недвижимости
    # images_urls = soup.find('div', id='slidePhoto').find('input', id='hidUrlsPhotos').get('value').split('|')
    # print(type(images_urls))
    # print(images_urls)

    house_data_row = {'Title': title, 'Adresss': adress, 'Property Type': type_of_house, 'Rooms': habitaciones,
                      'Bathroom': bano, 'Planta': planta, 'Surface': surface_house, 'Price': price_house,
                      'Agency': agancy_name, 'Tel': telefon}
    print('READY: {}'.format(html))
    return house_data_row



def main():
    final_house_dataset = pd.DataFrame(columns=['Title', 'Adresss', 'Property Type', 'Rooms', 'Bathroom',
                                                'Planta', 'Surface', 'Price', 'Agency', 'Phone'])
    links = getPageLinks(1)
    print('links in page: ', len(links))

    for i in range(2):
        for p in range(2):
            try:
                fistrow = get_page_data(links[i])
                print(fistrow)
                final_house_dataset = final_house_dataset.append(fistrow, ignore_index=True)

                time.sleep(1)
                break
            except:
                print('Can\'t parse:', links[i])
                continue
    final_house_dataset.to_csv('HOUSEs3.csv')
if __name__ == '__main__':
    main()
