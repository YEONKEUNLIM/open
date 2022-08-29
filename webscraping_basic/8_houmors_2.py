import requests
from bs4 import BeautifulSoup
import sqlite3

url = "http://www.todayhumor.co.kr/board/list.php?table=humordata"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}
res = requests.get(url, headers=headers)
res.raise_for_status()


soup = BeautifulSoup(res.text, "lxml")

#고유번호 / 제목 / 링크 구하기
humors = soup.find_all("td", attrs={"class":"subject"})
for humor in humors :
    title = humor.a.get_text()
    link = humor.a["href"]
    ful_link = "http://www.todayhumor.co.kr" + link
    no = link.split("&")[1].replace("no=","")
    print(no,title,link)



con = sqlite3.connect

