from time import sleep
from typing import KeysView
from xml.dom.minidom import Attr
from selenium import webdriver
from selenium.webdriver.common.by import By

#m = p.match("care") # match : 주어진 문자열의 처음부터 일치하는지 확인
#print_match(m)

#browser = webdriver.Chrome()#"C:\open\webscraping_basic\chromedriver.exe"
#browser.get("https://creators.kakao.com/")

#from selenium import webdriver
#browser = webdriver.Chrome()
#browser.get("https://creators.kakao.com/")
#elem = browser.find_element(By.CLASS_NAME, "link_login").click()
#from selenium.webdriver.common.keys import Keys
#loginId = browser.find_element(By.ID, "id_email_2")
#loginId.send_keys("01091300112")
#pwd = browser.find_element(By.ID,"id_password_3")
#pwd.send_keys("sksmsdus11!!")
#browser.find_element(By.CLASS_NAME,"recaptcha-checkbox").click()
#browser.find_element(By.CLASS_NAME,"btn_confirm").click()

#from selenium import webdriver
#browser = webdriver.Chrome()
#browser.get("https://creators.kakao.com/")
#elem = browser.find_element(By.CLASS_NAME, "link_login").click()
#from selenium.webdriver.common.keys import Keys

################# DB GET START ##################

#추가할 보드 url
boardUrl = "channel/_Shxnlxj/dashboard"

#보드 제목
title = "제목 테스트"
#보드 설명
comment = "설명 테스트"
#링크
contentsLink = "http://www.todayhumor.co.kr/board/view.php?table=humorbest&no=1705463"

#카테고리 19 : humor
category = "19"

################## DB GET END ###################

################# KAKAO LOG IN START ############
#kakao 창작 Url
kakaoUrl = "https://creators.kakao.com/"

#브라우저 객체 생성
browser = webdriver.Chrome()
#카카오 창작소 open
browser.get(kakaoUrl)

#로그인창 접속
browser.find_element(By.CLASS_NAME, "link_login").click()

#로그인 접속 정보 입력
browser.find_element(By.ID, "id_email_2").send_keys("01091300112")
browser.find_element(By.ID,"id_password_3").send_keys("sksmsdus00!!!")
sleep(1)
#로그인
browser.find_element(By.CLASS_NAME,"btn_confirm").click()

#로그인 인증까지 대기시간 필요
sleep(10)
################# KAKAO LOG IN END ##############

################# 보드 발행 START ################
#보드 대시보드 이동
browser.get(kakaoUrl+boardUrl)
sleep(3)
#보드 등록
browser.find_element(By.CLASS_NAME,"link_newboard").click()
sleep(1)
#보드 제목 입력
boardTitle = browser.find_element(By.ID, "boardTitle")
boardTitle.send_keys(title)
sleep(1)
#보드 설명 입력
boardCmt = browser.find_element(By.ID, "boardCmt")
boardCmt.send_keys(comment)
sleep(1)
#보드 링크 탭 선택
browser.find_element(By.XPATH,"//*[@id='mainContent']/div[2]/div/div[2]/div[2]/ul/li[2]/a").click()
sleep(1)
#링크 입력
url = browser.find_element(By.NAME, "url")
url.send_keys(contentsLink)
sleep(1)
#링크 검색
browser.find_element(By.CLASS_NAME,"btn_search").click()
sleep(3)
#보드 담기
browser.find_element(By.XPATH,"//*[@id='mainContent']/div[2]/div/div[2]/div[3]/form/div[2]/ul/li/div[2]/button").click()
sleep(2)
#발행하기
browser.find_element(By.XPATH,"//*[@id='mainContent']/div[3]/div[2]/button[2]").click()
sleep(2)
#발행설정 > 카테고리(선택)
browser.find_element(By.XPATH,"//*[@id='layer']/div/div/div[2]/div/div[3]/dl/dd/div/div["+category+"]/label").click()
sleep(1)
#최종 발행하기
browser.find_element(By.XPATH,"//*[@id='layer']/div/div/div[2]/div/div[5]/button[2]").click()
sleep(5)
#오픈전 팝업나올때 처리.
#browser.find_element(By.XPATH,"//*[@id='layer']/div/div/div[3]/div/button").click()
browser.execute_script("document.getElementsByClassName('btn_g btn_primary')[1].click()")

################# 보드 발행 END ##################
