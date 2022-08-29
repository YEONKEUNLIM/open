import requests
url = "http://www.todayhumor.co.kr/board/list.php?table=humorbest"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}
res = requests.get(url, headers)
res.raise_for_status()
with open("myHumor.html","w", encoding="utf8") as f:
    f.write(res.text)