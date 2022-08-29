import requests
from bs4 import BeautifulSoup

url = "http://www.todayhumor.co.kr/board/list.php?table=humorbest"
res = requests.get(url)
res.raise_for_status()


soup = BeautifulSoup(res.text, "lxml")
#print(soup.title)
#print(soup.title.get_text())
#print(soup.a) #soup 객체에서 처음 바견되는 a element 출력
#print(soup.a.attrs) # a element 의 속성 정보를 출력
#print(soup.a["href"]) # a element 의 href 속성 '값' 정보를 출력

#print(soup.find("td > a", attrs={"class" : "subject"})) #클래스가 subject인 element를 찾아줘

#print(soup.find("td", attrs={"class" : "subject"}))
#rank1 = soup.find("tr", attrs={"class" : "view list_tr_humordata"})
#print(rank1.get_text())

humor = soup.find("a", text = "놀이공원에 놀러간 전투기 조종사")
print(humor)