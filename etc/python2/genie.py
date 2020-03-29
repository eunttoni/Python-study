import requests
import bs4

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
r = requests.get("https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200309", headers=headers)
soap = bs4.BeautifulSoup(r.text, 'html.parser')

# 순위 / 곡 제목 / 가수 (네이버영화 실습과 동일하게 진행)
# array = [soap.select("td.info > a.title.ellipsis"), soap.select("td.info > a.artist.ellipsis")]

num = 0;
lists = soap.select("tbody tr.list")
for a in lists:
    num = num + 1;
    title = a.select("a.title.ellipsis")
    artist = a.select("a.artist.ellipsis")
    print(num, "/ ",title[0].text.strip()," / ",artist[0].text)

