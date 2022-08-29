from http.client import CONTINUE
from pydoc import importfile
from re import sub
import requests
from bs4 import BeautifulSoup
from ast import Try
from asyncio.windows_events import NULL
from concurrent.futures import thread
from socket import create_connection
import threading
from time import sleep, time
from typing import KeysView
from warnings import catch_warnings
from xml.dom.minidom import Attr
from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3
from sqlite3 import Error
import re

def humorSearch(conn, param) :
    siteNo = param[1]
    default_url = param[3]
    sub_url = param[4]
    boardNm = param[0]
    category = param[2]

    url = default_url+sub_url
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")

    #고유번호 / 제목 / 링크 구하기
    #humors = soup.find_all("td", attrs={"class":"subject"})
    humors = soup.find_all("tr", class_="view list_tr_humordata")
    
    #humors = soup.find_all("td", class_="list_tr_humordata subject")
    for humor in humors :
        
        #title = humor.a.get_text()
        #link = humor.a["href"]
        title = humor.find("td",attrs={"class":"subject"}).a.get_text()
        link = humor.find("td",attrs={"class":"subject"}).a["href"]

        ful_link = default_url + link
        no = link.split("&")[1].replace("no=","")
        comment = ""
        #site, no, title로 중복 안된 것만 insert 한다.
        print("################# 타이틀 필터 START ##################")
        finter = reg_filter_title(title)
        print("#################",finter)
        if finter != None :
            print("################# 타이틀 필터에 의해 SKIPT ##################", title)
            continue
        print("################# 타이틀 필터 END ##################")
 
        print("################# 중복체크 START ##################")
        cnt = validation_check(conn, siteNo, no, title).fetchone()[0]
        print("중복 Count : ",cnt)
        print("################## 중복체크 END ###################")
        if cnt == 0 :
            print("중복된 데이터가 없습니다. insert")
            insert_link_info(conn, siteNo, boardNm, no, title, comment, ful_link, category)

        else :
            print("중복된 데이터가 있습니다. skip")
        print(no,title,link)

#TITLE FILTER
def reg_filter_title(title) :
    print("#################1 ##################")
    filterLit = ["ㅇㅎ","ㅇ ㅎ","혐","후방","후 방","약후","약 후","ㅎㅂ","ㅎ ㅂ","도끼"]
    for filter in filterLit :
        p = re.compile(filter) 
        print("#################2 ##################")
        m = p.search(title)
        if m != None :
            print("aaa",m)
            return m
        print("#################3##################",m)
    return m 

#LINK_INFO INSERT
def insert_link_info(conn, siteNo, boardNm, no, title, comment, ful_link, category):
    print("################# LINK_INFO INSERT START ##################")
    print(siteNo, boardNm, no, title, comment, ful_link, category)
    sql = "insert into LINK_INFO(SITE_NO, BOARD_NAME, NUMBER, TITLE, COMMENT, FULL_LINK, CATEGORY)values(?,?,?,?,?,?,?)"
    cur = conn.cursor()
    cur.execute(sql, (siteNo, boardNm, no, title, comment, ful_link, category))
    conn.commit()
    print("################## LINK_INFO INSERT END ###################")
    return cur

#중복 체크
def validation_check(conn, siteNo, no, title):
    print("################# DB GET START ##################")
    print(siteNo, no, title)
    sql = "select COUNT(LINK_NO) CNT from LINK_INFO WHERE ((SITE_NO = ? AND NUMBER = ?) OR  (TITLE = ?))"
    cur = conn.cursor()
    cur.execute(sql, (siteNo, no, title))
    print("################## DB GET END ###################")
    return cur

#데이터 조회
def get_site_info(conn):
    print("################# DB GET START ##################")
    sql = "select A.BOARD_NAME, B.SITE_NO, A.CATEGORY,  B.DEFAULT_URL, B.URL1 from BOARD_MASTER A LEFT OUTER JOIN SITE_MASTER B WHERE A.BOARD_NAME = B.BOARD_NAME AND A.USE_YN = 'Y' AND B.USE_YN = 'Y' AND A.CUR_CNT < A.MAX_CNT"
    cur = conn.cursor()
    cur.execute(sql)
    #conn.close()
    #cur.close()
    print("################## DB GET END ###################")
    return cur

def search_run(conn) :
    list = get_site_info(conn)

    if list == [] :
        print("site 정보가 없습니다. skip", list)

    #각 사이트 별 조회
    for data in list :
        if data[0] == "꿀잼창고" :
            #1:오늘의 유머, 2:기타
            if data[1] == 1 :
                print("111111111")
                humorSearch(conn, data)
                print("222222222")
            elif data[1] == 2 :
                print("")

        elif data[0] =="먹깨비" :
            #1:오늘의 유머, 2:기타
            if data[1] == 1 :
                print("")
        elif data[0] == "꿀잼창고2" :
            #1:오늘의 유머, 2:기타
            if data[1] == 1 :
                print("")
        elif data[0] == "꿀잼창고2" :
            #1:오늘의 유머, 2:기타
            if data[1] == 1 :
                print("")
        elif data[0] == "꿀잼창고3" :
            #1:오늘의 유머, 2:기타
            if data[1] == 1 :
                print("")
        elif data[0] == "꿀잼창고4" :
            #1:오늘의 유머, 2:기타
            if data[1] == 1 :
                print("")
        elif data[0] == "꿀잼창고5" :
            #1:오늘의 유머, 2:기타
            if data[1] == 1 :
                print("")
        elif data[0] == "꿀잼창고6" :
            #1:오늘의 유머, 2:기타
            if data[1] == 1 :
                print("")
        elif data[0] == "꿀잼창고7" :
            #1:오늘의 유머, 2:기타
            if data[1] == 1 :
                print("")
        elif data[0] == "꿀잼창고8" :
            #1:오늘의 유머, 2:기타
            if data[1] == 1 :
                print("")

def main() : 

    print("DB 드라이버 연결")
    database = r"d:\sqLiteDataBase\kakaoBoard.db"
    conn = sqlite3.connect(database)
   
    with conn :
        print("-------start-------")
        bTrue = True
        while bTrue :
            try :
                search_run(conn)
                
                #60초에 한번 데이터 조회하여 실행
                sleep(60)
            except Exception as e :
                print("board 시작시(board_run) 예외가 발생 했습니다.", e)
                #현재 세션의 브라우저만 종료
                #browser.close() 
                #전체 세션의 브라우저 종료
                #browser.quit()
                bTrue = False
            sleep(300) #5분
            #sleep(3600) #60분
        print("--------end------")

if __name__ == '__main__':
    main()