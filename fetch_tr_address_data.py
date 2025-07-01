import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.postakodu.web.tr/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": BASE_URL
}

session = requests.Session()
session.headers.update(HEADERS)

def get_city_links(retries=3):
    for attempt in range(retries):
        try:
            resp = session.get(BASE_URL)
            resp.encoding = resp.apparent_encoding
            soup = BeautifulSoup(resp.text, "html.parser")
            city_links = []
            for a in soup.select("div#liste3 ul#links2 li a.poko"):
                href = a.get("href")
                name = a.text.strip().replace(" Posta Kodu", "")
                if href and name:
                    city_links.append((name, BASE_URL + href.lstrip("/")))
            return city_links
        except Exception as e:
            print(f"Hata (şehir linkleri): {BASE_URL} - {e}")
            if attempt < retries - 1:
                time.sleep(3)
            else:
                with open("failed_city_links.txt", "a", encoding="utf-8") as logf:
                    logf.write(f"{BASE_URL} - {e}\n")
                return []

def get_district_links(city_url, retries=3):
    for attempt in range(retries):
        try:
            resp = session.get(city_url)
            resp.encoding = resp.apparent_encoding
            soup = BeautifulSoup(resp.text, "html.parser")
            district_links = []
            for a in soup.select("div#cont ul#links3 li a.poko"):
                href = a.get("href")
                name = a.text.strip()
                if href and name:
                    district_links.append((name, BASE_URL + href.lstrip("/")))
            return district_links
        except Exception as e:
            print(f"Hata (ilçe linkleri): {city_url} - {e}")
            if attempt < retries - 1:
                time.sleep(3)
            else:
                with open("failed_district_links.txt", "a", encoding="utf-8") as logf:
                    logf.write(f"{city_url} - {e}\n")
                return []

def get_quarters_and_neighborhoods(district_url, retries=3):
    for attempt in range(retries):
        try:
            resp = session.get(district_url)
            resp.encoding = resp.apparent_encoding
            soup = BeautifulSoup(resp.text, "html.parser")
            quarters = []
            for a in soup.select("div#cont ul#links3 li a.poko"):
                href = a.get("href")
                name = a.text.strip()
                if href and name:
                    quarters.append((name, BASE_URL + href.lstrip("/")))
            return quarters
        except Exception as e:
            print(f"Hata (semt/mahalle): {district_url} - {e}")
            if attempt < retries - 1:
                time.sleep(3)
            else:
                with open("failed_quarters.txt", "a", encoding="utf-8") as logf:
                    logf.write(f"{district_url} - {e}\n")
                return []

def get_neighborhoods(quarter_url, retries=3):
    for attempt in range(retries):
        try:
            resp = session.get(quarter_url)
            resp.encoding = resp.apparent_encoding
            soup = BeautifulSoup(resp.text, "html.parser")
            neighborhoods = []
            for a in soup.select("div#cont ul#links3 li a.poko"):
                href = a.get("href")
                name = a.text.strip()
                if href and name:
                    neighborhoods.append((name, BASE_URL + href.lstrip("/")))
            return neighborhoods
        except Exception as e:
            print(f"Hata (mahalle): {quarter_url} - {e}")
            if attempt < retries - 1:
                time.sleep(3)
            else:
                with open("failed_neighborhoods.txt", "a", encoding="utf-8") as logf:
                    logf.write(f"{quarter_url} - {e}\n")
                return []

def get_postcode(neighborhood_url, retries=3):
    for attempt in range(retries):
        try:
            resp = session.get(neighborhood_url)
            resp.encoding = resp.apparent_encoding
            soup = BeautifulSoup(resp.text, "html.parser")
            h2 = soup.select_one("div#pstkd2 h2")
            if h2 and h2.text.strip():
                return h2.text.strip()
            return None
        except Exception as e:
            print(f"Hata (posta kodu): {neighborhood_url} - {e}")
            if attempt < retries - 1:
                time.sleep(3)  # Biraz bekle ve tekrar dene
            else:
                # Son denemede de hata olursa logla
                with open("failed_postcodes.txt", "a", encoding="utf-8") as logf:
                    logf.write(f"{neighborhood_url} - {e}\n")
                return None

def main():
    result = []
    cities = get_city_links()
    for city_name, city_url in cities:
        print(f"Şehir: {city_name}")
        city_obj = {"name": city_name, "districts": []}
        districts = get_district_links(city_url)
        for district_name, district_url in districts:
            print(f"  İlçe: {district_name}")
            district_obj = {"name": district_name, "quarters": []}
            quarters = get_quarters_and_neighborhoods(district_url)
            for quarter_name, quarter_url in quarters:
                print(f"    Semt: {quarter_name}")
                quarter_obj = {"name": quarter_name, "neighborhoods": []}
                neighborhoods = get_neighborhoods(quarter_url)
                for neighborhood_name, neighborhood_url in neighborhoods:
                    print(f"      Mahalle: {neighborhood_name}")
                    postcode = get_postcode(neighborhood_url)
                    print(f"        Posta Kodu: {postcode}")
                    quarter_obj["neighborhoods"].append({
                        "name": neighborhood_name,
                        "postcode": postcode
                    })
                    time.sleep(0.1)
                district_obj["quarters"].append(quarter_obj)
                time.sleep(0.2)
            city_obj["districts"].append(district_obj)
            time.sleep(1)
        result.append(city_obj)
        time.sleep(1)
    with open("tr-address-data.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("Veri çekme tamamlandı. Sonuç: tr-address-data.json")

if __name__ == "__main__":
    main() 