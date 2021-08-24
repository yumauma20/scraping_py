import requests
from bs4 import BeautifulSoup
import time
import pandas as pd


def get_page_text(url):
    """ 指定したURLのhtmlを取得する """
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


base_url = "https://suumo.jp"

url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=14&sc=14131&sc=14132&sc=14133&sc=14134&sc=14135&sc=14136&sc=14137&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1"
soup = get_page_text(url)

a_tags = []
a_tags = soup.find_all(
    "a", class_="js-cassette_link_href cassetteitem_other-linktext")

all_data = []
for a_tag in a_tags:
    data = {}

    # 詳細ページのURL取得
    href = a_tag.get("href")
    detail_link = base_url + href
    soup = get_page_text(detail_link)

    data["house_name"] = soup.select_one(
        ".section_h1-header-title").getText()

    data["rent"] = soup.select_one(
        ".property_view_note-emphasis").getText()

    data["management_common_fee"] = soup.select_one(
        ".property_view_note-info > div:nth-of-type(1) > span:nth-of-type(2)").getText()[9:]

    data["security_deposit"] = soup.select_one(
        ".property_view_note-info > div:nth-of-type(2) > span:nth-of-type(1)").getText()[4:]

    data["key_money"] = soup.select_one(
        ".property_view_note-info > div:nth-of-type(2) > span:nth-of-type(2)").getText()[4:]

    data["deposit"] = soup.select_one(
        ".property_view_note-info > div:nth-of-type(2) > span:nth-of-type(3)").getText()[5:]

    data["laying_depreciation"] = soup.select_one(
        ".property_view_note-info > div:nth-of-type(2) > span:nth-of-type(4)").getText()[7:]

    # テーブルのデータ取得
    property_view_table_tds = soup.select_one(
        ".property_view_table").find_all("td")

    data["location"] = property_view_table_tds[0].getText()
    data["from_station"] = property_view_table_tds[1].getText()
    data["floor_plan"] = property_view_table_tds[2].getText()
    data["occupied_area"] = property_view_table_tds[3].getText()
    data["age"] = property_view_table_tds[4].getText()
    data["floor"] = property_view_table_tds[5].getText()
    data["direction"] = property_view_table_tds[6].getText()
    data["kinds"] = property_view_table_tds[7].getText()
    data["url"] = detail_link
    all_data.append(data)
    ''' time.sleep(3) '''

print(all_data)
# df = pd.DataFrame()
