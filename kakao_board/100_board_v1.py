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


kakaoUrl = "https://creators.kakao.com/" #kakao 창작 Url
browser = NULL #브라우저 객체 생성
boardUrl = "" #추가할 보드 url
title = "" #보드 제목
comment = "" #보드 설명
contentsLink = "" #링크
category = "" #카테고리 19 : humor


#카카오 로그인
def kakao_login(m):
    if m :
        print("################# KAKAO LOG IN START ############")
        print("브라우저 객체 생성")
        browser = webdriver.Chrome()
        
      
        print("경고창 unload 처리")
    
        print("카카오 창작소 open")
        browser.get(kakaoUrl)

        print("카로그인창 접속")
        browser.find_element(By.CLASS_NAME, "link_login").click()

        print("로그인 접속 정보 입력")
        browser.find_element(By.ID, "id_email_2").send_keys("01091300112")
        browser.find_element(By.ID,"id_password_3").send_keys("sksmsdus00!!!")
        sleep(1)
        print("로그인")
        browser.find_element(By.CLASS_NAME,"btn_confirm").click()

        print("로그인 인증까지 대기시간 필요")
        sleep(10)
        print("################# KAKAO LOG IN END ##############")

        return browser
    else :
        browser.quit()
        print("====browser.close()====")

#DB 연결
def data_connection(db_file):
    conn = None

    try :
        conn = sqlite3.connect(db_file)

    except Error as e :
        print(e)

    return conn

#데이터 조회
def data_search(conn):
    print("################# DB GET START ##################")
    sql = "SELECT A.BOARD_NAME, A.BOARD_URL, B.TITLE, B.COMMENT, B.FULL_LINK, B.CATEGORY, B.LINK_NO FROM 'BOARD_MASTER' A LEFT OUTER JOIN 'LINK_INFO' B WHERE A.BOARD_NAME = B.BOARD_NAME AND A.CATEGORY = B.CATEGORY AND A.USE_YN = 'Y' AND B.USE_YN = 'Y' AND B.UPLOAD_FLAG = 'N' AND A.CUR_CNT < A.MAX_CNT ORDER BY A.BOARD_NAME, B.LINK_NO"
    cur = conn.cursor()
    cur.execute(sql)
    #conn.close()
    #cur.close()
    print("################## DB GET END ###################")
    return cur


#데이터 조회
def check_board_full(conn, boardNm):
    print("################# DB GET START ##################")
    sql = "select COUNT(BOARD_NAME)AS CNT from BOARD_MASTER where BOARD_NAME = ? AND CUR_CNT >= MAX_CNT"
    cur = conn.cursor()
    cur.execute(sql,(boardNm,))
    #conn.close()
    #cur.close()
    print("################## DB GET END ###################")
    return cur




#보드 등록
def insert_board(conn, data, browser, CurCount, MaxCount):
    
    print(data)
    print("browser session : ",browser)
    print("추가할 보드 url")
    boardUrl = data[1] #boardUrl = "channel/_Shxnlxj/dashboard"
    print("보드 제목")
    title = data[2] #title = "제목 테스트"
    print("보드 설명")
    comment = data[3] #comment = "설명 테스트"
    print("링크")
    contentsLink = data[4] #contentsLink = "http://www.todayhumor.co.kr/board/view.php?table=humorbest&no=1705463"

    print("카테고리 19 : humor")
    category = str(data[5]) #category = "19"

    if CurCount == 0 : 
        print("################# 보드 발행 START ################")
        print("보드 대시보드 이동")
        browser.get(kakaoUrl+boardUrl)

        sleep(3)
        print("보드 등록")
        browser.find_element(By.CLASS_NAME,"link_newboard").click()

        #만약 10개 보드로 꽉찼으면? 팝업 닫고 continue 진행한다. 

        sleep(1)
        print("보드 제목 입력")
        boardTitle = browser.find_element(By.ID, "boardTitle")
        boardTitle.send_keys(title)
        sleep(1)
        print("보드 설명 입력")
        boardCmt = browser.find_element(By.ID, "boardCmt")
        boardCmt.send_keys(comment)
        sleep(1)
        print("보드 링크 탭 선택")
        browser.find_element(By.XPATH,"//*[@id='mainContent']/div[2]/div/div[2]/div[2]/ul/li[2]/a").click()
        sleep(1)
    
    if CurCount > 0 :
        sleep(1)
        print("링크 삭제")
        browser.find_element(By.CLASS_NAME,"btn_del").click()
        
    
    print("링크 입력")
    url = browser.find_element(By.NAME, "url")
    url.send_keys(contentsLink)

    sleep(1)
    print("링크 검색")
    browser.find_element(By.CLASS_NAME,"btn_search").click()
    sleep(3)
    print("보드 담기")
    browser.find_element(By.XPATH,"//*[@id='mainContent']/div[2]/div/div[2]/div[3]/form/div[2]/ul/li/div[2]/button").click()
    
    CurCount = CurCount+1
    if CurCount == MaxCount : 
        sleep(2)
        print("발행하기")
        browser.find_element(By.XPATH,"//*[@id='mainContent']/div[3]/div[2]/button[2]").click()
        sleep(2)
        print("발행설정 > 카테고리(선택)")
        browser.find_element(By.XPATH,"//*[@id='layer']/div/div/div[2]/div/div[3]/dl/dd/div/div["+category+"]/label").click()
        sleep(1)
        print("최종 발행하기")
        browser.find_element(By.XPATH,"//*[@id='layer']/div/div/div[2]/div/div[5]/button[2]").click()
        sleep(5)
        print("오픈전 팝업나올때 처리.")
        #browser.find_element(By.XPATH,"//*[@id='layer']/div/div/div[3]/div/button").click()
        popupTxt = browser.find_element(By.XPATH,"//*[@id='layer']/div/div/div[1]/strong").text
        print(popupTxt)
        if popupTxt == '하루에 너무 많은 보드를 발행하고 있어요.':
            #DB에 해당 보드 개수 10 만들기
            print("#############BOARD_MASTER 현재 발생 개수 최대치 개수로 수정 START#############")
            add_complete_update2(conn, data[0])
            print("#############BOARD_MASTER 현재 발생 개수 최대치 개수로 수정 END#############")
            #팝업 Close
            browser.execute_script("document.getElementsByClassName('btn_g btn_primary')[1].click()")
            sleep(1)
            #현재창 초기화
            browser.find_element(By.XPATH,"//*[@id='root']/div[2]/main/section/aside/nav/ul/li[2]/a").click()
            sleep(1)
            browser.find_element(By.XPATH,"//*[@id='layer']/div/div/div[3]/div/button[2]").click()
            
        else :
            
            print("#############LINK_INFO UPLOAD_FLAG Y 처리 & BOARD_MASTER Count + 1 START#############")
            add_complete_update1(conn, data[0], data[6])
            print("#############LINK_INFO UPLOAD_FLAG Y 처리 & BOARD_MASTER Count + 1 END#############")

            browser.execute_script("document.getElementsByClassName('btn_g btn_primary')[1].click()")


    print("################# 보드 발행 END ##################")

    return CurCount

#Main() Board 발행 횟수 초기화 
def init_board_curcnt_zero(conn) :

    cur = conn.cursor()

    cur.execute("UPDATE 'BOARD_MASTER' SET CUR_CNT = 0 WHERE USE_YN = 'Y' ")
    conn.commit()


#BOARD COUNT + 1 AND LINK_INP UPDATE = Y처리
def add_complete_update1(conn, boardNm, linkNo) :

    cur = conn.cursor()

    cur.execute("UPDATE 'BOARD_MASTER' SET CUR_CNT = CUR_CNT + ? WHERE BOARD_NAME = ?",(1,str(boardNm)))
    conn.commit()

    cur.execute("UPDATE 'LINK_INFO' SET UPLOAD_FLAG = 'Y' WHERE LINK_NO = ?", (int(linkNo),))
    conn.commit()

    #conn.close()
    #cur.close()

#BOARD 현개 발행 개수 MAX_COUNT로 처리
def add_complete_update2(conn, boardNm) :

    cur = conn.cursor()

    cur.execute("UPDATE 'BOARD_MASTER' SET CUR_CNT = MAX_CNT WHERE BOARD_NAME = ?",(str(boardNm),))
    conn.commit()

    #conn.close()
    #cur.close()

def board_run(conn,browser) : 

    print("board_run start")

    data = data_search(conn).fetchall()
  
    if data == [] :
        print("등록된 data가 없습니다. skip", data)
    
    curCount = 0
    maxCount = 5
    #카카오 보드에 입력
    for tmp in data :
        print("보드 발행 max 인지 체크 시작", tmp)
        cnt = check_board_full(conn, tmp[0]).fetchone()[0]
        print("0 : 보드 발행 가능, 1:보드 Full 발행 불가능 : ",cnt)
        print("보드 발행 max 인지 체크 종료")
        
        if cnt > 0 :
            continue
        else :
            curCount = insert_board(conn,tmp,browser, curCount, maxCount)
        
        if curCount == maxCount : 
            curCount = 0
            #try :
            #    insert_board(tmp,browser)
            #except Exception as e :
            #    print("카카오 보드에 입력 시 (insert_board) 예외가 발생 했습니다", e)

    print("board_run end")

def main() : 


    print("DB 드라이버 연결")
    database = r"d:\sqLiteDataBase\kakaoBoard.db"
    conn = sqlite3.connect(database)
   

    with conn :
        print("-------start-------")
        print("현재 보드 횟수 초기화 시작")
        init_board_curcnt_zero(conn)
        print("현재 보드 횟수 초기화 종료")
        print("카카오 화면 띄우기")
        bTrue = False
        while bTrue == False :

            bTrue = True
            browser = kakao_login(bTrue)

            while bTrue : 
                try :
                    board_run(conn,browser)

                    #60초에 한번 데이터 조회하여 실행
                    sleep(60)
                except Exception as e :
                    print("board 시작시(board_run) 예외가 발생 했습니다.", e)
                    #현재 세션의 브라우저만 종료
                    #browser.close() 
                    #전체 세션의 브라우저 종료
                    browser.quit()
                    bTrue = False

            sleep(3600) #60분
            #sleep(60) #1분

        print("--------end------")

if __name__ == '__main__':
    main()


