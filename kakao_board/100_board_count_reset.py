import sqlite3
from sqlite3 import Error

#DB 연결
def data_connection(db_file):
    conn = None

    try :
        conn = sqlite3.connect(db_file)

    except Error as e :
        print(e)

    return conn

#Main() Board 발행 횟수 초기화 
def init_board_curcnt_zero(conn) :

    cur = conn.cursor()

    cur.execute("UPDATE 'BOARD_MASTER' SET CUR_CNT = 0 WHERE USE_YN = 'Y' ")
    conn.commit()
    
def main() : 

    print("DB 드라이버 연결")
    database = r"d:\sqLiteDataBase\kakaoBoard.db"
    conn = sqlite3.connect(database)
    
    with conn :
        print("-------start-------")
        bTrue = True
        while bTrue :
            try :
                print("-------start-------")
                print("현재 보드 횟수 초기화 시작")
                init_board_curcnt_zero(conn)
                print("현재 보드 횟수 초기화 종료")
                #os.system('pause')
                #input()
                #60초에 한번 데이터 조회하여 실행
                #sleep(60)
                quit()
                
            except Exception as e :
                print("예외가 발생 했습니다.", e)
                #현재 세션의 브라우저만 종료
                #browser.close() 
                #전체 세션의 브라우저 종료
                #browser.quit()
                bTrue = False
                quit()
                
            sleep(300) #5분
            #sleep(3600) #60분
        print("--------end------")

if __name__ == '__main__':
    main()