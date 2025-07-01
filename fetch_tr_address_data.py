import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = httpspostakodu.ptt.gov.tr
session = requests.Session()

def get_hidden_inputs(soup)
    data = {}
    for inp in soup.find_all(input, type=hidden)
        data[inp[name]] = inp.get(value, )
    return data

def get_select_options(soup, name)
    select = soup.find(select, {name name})
    if not select
        return []
    return [
        (option[value], option.text.strip())
        for option in select.find_all(option)
        if option[value] != -1
    ]

# 1. İlk GET Sayfa ve hidden inputlar
resp = session.get(BASE_URL)
soup = BeautifulSoup(resp.text, html.parser)
hidden = get_hidden_inputs(soup)
cities = get_select_options(soup, ctl00$MainContent$DropDownList1)

result = []

for city_id, city_name in cities
    print(fŞehir {city_name})
    # 2. İl seçimi için POST
    data = hidden.copy()
    data[ctl00$MainContent$DropDownList1] = city_id
    data[__EVENTTARGET] = ctl00$MainContent$DropDownList1
    resp = session.post(BASE_URL, data=data)
    soup = BeautifulSoup(resp.text, html.parser)
    hidden = get_hidden_inputs(soup)
    districts = get_select_options(soup, ctl00$MainContent$DropDownList2)
    city_obj = {name city_name, districts []}

    for district_id, district_name in districts
        print(f  İlçe {district_name})
        # 3. İlçe seçimi için POST
        data2 = hidden.copy()
        data2[ctl00$MainContent$DropDownList1] = city_id
        data2[ctl00$MainContent$DropDownList2] = district_id
        data2[__EVENTTARGET] = ctl00$MainContent$DropDownList2
        resp2 = session.post(BASE_URL, data=data2)
        soup2 = BeautifulSoup(resp2.text, html.parser)
        hidden2 = get_hidden_inputs(soup2)
        neighborhoods = get_select_options(soup2, ctl00$MainContent$DropDownList3)
        district_obj = {name district_name, neighborhoods []}

        for neighborhood_id, neighborhood_name in neighborhoods
            print(f    Mahalle {neighborhood_name})
            # 4. Mahalle seçimi için POST
            data3 = hidden2.copy()
            data3[ctl00$MainContent$DropDownList1] = city_id
            data3[ctl00$MainContent$DropDownList2] = district_id
            data3[ctl00$MainContent$DropDownList3] = neighborhood_id
            data3[__EVENTTARGET] = ctl00$MainContent$DropDownList3
            resp3 = session.post(BASE_URL, data=data3)
            soup3 = BeautifulSoup(resp3.text, html.parser)
            # Posta kodu sayfanın belirli bir yerinde span veya label içinde olabilir
            pk_span = soup3.find(span, {id MainContent_Label1})
            postcodes = []
            if pk_span and pk_span.text.strip()
                postcodes = [pk_span.text.strip()]
            district_obj[neighborhoods].append({
                name neighborhood_name,
                postcodes postcodes
            })
            time.sleep(0.1)  # Sunucuyu yormamak için kısa bekleme

        city_obj[districts].append(district_obj)
        time.sleep(0.1)
    result.append(city_obj)
    time.sleep(0.2)

with open(tr-address-data.json, w, encoding=utf-8) as f
    json.dump(result, f, ensure_ascii=False, indent=2)

print(Veri çekme tamamlandı. Sonuç tr-address-data.json) 