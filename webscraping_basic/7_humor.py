import requests
from bs4 import BeautifulSoup

url = "http://www.todayhumor.co.kr/board/list.php?table=humorbest"
res = requests.get(url)
res.raise_for_status()


soup = BeautifulSoup(res.text, "lxml")

humors = soup.find_all("td", attrs={"class":"subject"})
for humor in humors :
    print(humor.get_text())