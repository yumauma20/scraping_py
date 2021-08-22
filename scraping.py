import requests
from bs4 import BeautifulSoup

base_url = "https://suumo.jp"

# url変数に検索条件を反映させたURLを記載する
url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=14&sc=14131&sc=14132&sc=14133&sc=14134&sc=14135&sc=14136&sc=14137&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1"

res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

a_tags = []
a_tags = soup.find_all(
    "a", class_="js-cassette_link_href cassetteitem_other-linktext")

for a_tag in a_tags:
    # 詳細ページのURL取得
    href = a_tag.get("href")
    detail_link = base_url + href
    print(detail_link)
