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

# ここにデータ取得したい一覧ページのURLを貼る
url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=14&sc=14131&sc=14132&sc=14133&sc=14134&sc=14135&sc=14136&sc=14137&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1"
soup = get_page_text(url)

a_tags = []
a_tags = soup.find_all(
    "a", class_="js-cassette_link_href cassetteitem_other-linktext")

all_data = []
for a_tag in a_tags:
    data = []

    # 詳細ページのURL取得
    href = a_tag.get("href")
    detail_link = base_url + href
    soup = get_page_text(detail_link)

    data.append(soup.select_one(
        ".section_h1-header-title").getText())

    data.append(soup.select_one(
        ".property_view_note-emphasis").getText())

    data.append(soup.select_one(
        ".property_view_note-info > div:nth-of-type(1) > span:nth-of-type(2)").getText()[9:])

    data.append(soup.select_one(
        ".property_view_note-info > div:nth-of-type(2) > span:nth-of-type(1)").getText()[4:])

    data.append(soup.select_one(
        ".property_view_note-info > div:nth-of-type(2) > span:nth-of-type(2)").getText()[4:])

    data.append(soup.select_one(
        ".property_view_note-info > div:nth-of-type(2) > span:nth-of-type(3)").getText()[5:])

    data.append(soup.select_one(
        ".property_view_note-info > div:nth-of-type(2) > span:nth-of-type(4)").getText()[7:])

    # テーブルのデータ取得
    property_view_table_tds = soup.select_one(
        ".property_view_table").find_all("td")

    for i in range(len(property_view_table_tds)):
        data.append(property_view_table_tds[i].getText())

    data.append(detail_link)
    all_data.append(data)
    time.sleep(1)

df = pd.DataFrame(all_data, columns=["物件名", "家賃", "管理費・共益費", "敷金", "礼金", "保証金",
                  "敷引・償却", "所在地", "駅徒歩", "間取り", "専有面積", "築年数", "階", "向き", "建物種別", "リンク"])

df.to_excel('data/housing_information.xlsx', index=False,)

# //gittest