import requests

url = 'https://www.yahoo.co.jp/'
res = requests.get(url)

print(res.text[:500])
