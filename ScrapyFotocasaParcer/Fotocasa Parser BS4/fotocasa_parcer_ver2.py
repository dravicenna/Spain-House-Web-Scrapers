import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import time
import socks
import socket


# tor works
socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
socket.socket = socks.socksocket


main_url = 'https://www.fotocasa.es/es/comprar/viviendas/espana/todas-las-zonas/l/{}'


def checkIP():
    ip = requests.get('http://checkip.dyndns.org').content
    soup = BeautifulSoup(ip, 'html.parser')
    print(soup.find('body').text)


def getPageLinks(page_number):
    page_link = main_url.format(page_number)

    r = requests.get(page_link, headers={'User-Agent': UserAgent().chrome})
    if not r.ok:
        # если сервер нам отказал, вернем статус ошибки
        return r.status_code
    soup = BeautifulSoup(r.text, 'lxml')
    links = soup.findAll('a', attrs={'class': 're-Card-link'})
    first_link = 'https://www.fotocasa.es{}'
    links = [first_link.format(link.attrs['href']) for link in links]
    return links

def get_page_data(html):

    r = requests.get(html, headers={'User-Agent': UserAgent().chrome})
    if not r.ok:
        # если сервер нам отказал, вернем статус ошибки
        return r.status_code
    print('Status connect: ' + str(r.status_code))
    soup = BeautifulSoup(r.text, 'lxml')

    param = soup.findAll('script', attrs={'type': 'text/javascript'})

    param_str = str(param[2])
    param_str = param_str.split('{')[1]
    param_str = param_str.split('}')[0]
    # param_str = '{'+param_str+'}'.strip()

    my_dict = param_str.split('\r\n')
    # for i in range(len(my_dict)):
    #     print(my_dict[i].strip(), i)

    postal_code = my_dict[20].strip()[:-1].split(':')[-1].strip().replace('"', '')
    county = my_dict[10].strip()[:-1].split(':')[-1].strip().replace('"', '')
    city_zone = my_dict[8].strip()[:-1].split(':')[-1].strip().replace('"', '')
    city = my_dict[6].strip()[:-1].split(':')[-1].strip().replace('"', '')
    region_level1 = my_dict[60].strip()[:-1].split(':')[-1].strip().replace('"', '')
    region_level2 = my_dict[31].strip()[:-1].split(':')[-1].strip().replace('"', '')
    district = my_dict[48].strip()[:-1].split(':')[-1].strip().replace('"', '')
    neighbourhood = my_dict[18].strip()[:-1].split(':')[-1].strip().replace('"', '')
    street = my_dict[37].strip()[:-1].split(':')[-1].strip().replace('"', '')
    country = my_dict[45].strip()[:-1].split(':')[-1].strip().replace('"', '')
    surface_house = my_dict[15].strip()[:-1].split(':')[-1].strip().replace('"', '')
    surface_house_max = my_dict[16].strip()[:-1].split(':')[-1].strip().replace('"', '')
    surface_house_min = my_dict[17].strip()[:-1].split(':')[-1].strip().replace('"', '')
    rooms = my_dict[34].strip()[:-1].split(':')[-1].strip().replace('"', '')
    bathrooms = my_dict[43].strip()[:-1].split(':')[-1].strip().replace('"', '')
    price = my_dict[21].strip()[:-1].split(':')[-1].strip().replace('"', '')
    price_max = my_dict[22].strip()[:-1].split(':')[-1].strip().replace('"', '')
    price_min = my_dict[23].strip()[:-1].split(':')[-1].strip().replace('"', '')
    property_type = my_dict[24].strip()[:-1].split(':')[-1].strip().replace('"', '')
    property_state = my_dict[26].strip()[:-1].split(':')[-1].strip().replace('"', '')
    property_sub = my_dict[28].strip()[:-1].split(':')[-1].strip().replace('"', '')
    ad_publisher_type = my_dict[41].strip()[:-1].split(':')[-1].strip().replace('"', '')
    create_date = my_dict[47].strip()[:-1].replace('"', '').split('e: ')[-1]
    publish_date = my_dict[58].strip()[:-1].replace('"', '').split('e: ')[-1]
    transaction = my_dict[67].strip()[:-1].split(':')[-1].strip().replace('"', '')
    company = my_dict[71].strip()[:-1].split(':')[-1].strip().replace('"', '')
    # номер телефона
    telefon = soup.find('input', attrs={'name': 'ctl00$hid_AdPhone'})
    telefon = "" if not telefon else telefon.attrs['value'].strip().split(':')[-1].strip()
    link = html
    planta = soup.find('span', id='litFloor')
    planta = "" if not planta else planta.text.strip()

    data_row = {'postal_code': postal_code, 'county': county, 'city_zone':city_zone, 'city':city,
                'region_level1': region_level1, 'region_level2': region_level2, 'district': district,
                'neighbourhood': neighbourhood, 'street': street, 'country': country,
                'surface_house': surface_house, 'surface_house_max': surface_house_max,
                'surface_house_min': surface_house_min, 'planta': planta, 'rooms': rooms, 'bathrooms': bathrooms,
                'price': price, 'price_max': price_max, 'price_min': price_min, 'property_type': property_type,
                'property_state': property_state, 'property_sub': property_sub, 'ad_publisher_type':ad_publisher_type,
                'create_date': create_date, 'publish_date': publish_date, 'transaction': transaction,
                'company': company, 'telefon': telefon, 'link': link}
    return data_row

def main():
    final_house_dataset = pd.DataFrame(columns=['postal_code', 'county', 'city_zone', 'city', 'region_level1',
                                                'region_level2', 'district', 'neighbourhood', 'street', 'country',
                                                'surface_house', 'surface_house_max', 'surface_house_min', 'planta',
                                                'rooms', 'bathrooms', 'price', 'price_max', 'price_min',
                                                'property_type', 'property_state', 'property_sub', 'ad_publisher_type',
                                                'create_date', 'publish_date', 'transaction',
                                                'company', 'telefon', 'link'])

    links = getPageLinks(1)

    # for i in range(len(links)):
    for i in range(5):
        for p in range(5):
            try:
                fistrow = get_page_data(links[i])
                final_house_dataset = final_house_dataset.append(fistrow, ignore_index=True)
                print('Job: ', i)
                checkIP()
                time.sleep(2)
                break
            except:
                print('Can\'t parse:', links[i])
                continue
    final_house_dataset.to_csv('HOUSE.csv')
    # print(final_house_dataset)

if __name__ == '__main__':
    main()
