import sqlite3
import time

class SQL_CONNECT:
    def __init__(self):
        self.db_path = "D:\kiwoom_stock\KiwoomStock-Danta_Janny_bak/kiwoom_danta.db"  #DB경로
        self.nowdate = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    ##--------------------조회 기능--------------------------
    def SQL_UserSelect(self,tableNm):
        #회원 조회하기
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + tableNm ) 
        rows = cur.fetchall()
        user=[] 
        
        for row in rows:      
                  
            user = row
        conn.close()
        return user

    def SQL_GoldenCrossO(self):
        #5분봉 골든크로스 체크 O 조회
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM golden_cross_search WHERE S_CHECK = 'O'") 
        rows = cur.fetchall()
            
        item = []        
        count=0
        for row in rows:              
            item.insert(count,row) 
            count+=1
        conn.close()
        return(item)


    def SQL_StockOwn(self,sNum):
        #테이블 보유여부 판단
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM GOLDEN_CROSS_SEARCH WHERE S_NUM = '" + sNum+"'") 
        rows = cur.fetchall()
        
        rows = rows[0][0]
       
        conn.close()
        return rows



    ##--------------------삽입 기능--------------------------
    def SQL_GoldenCrossSearch(self,sqlString,sdata):
        #골든크로스 검색
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        print(sqlString, sdata)
        cur.execute(sqlString, sdata)
        conn.commit()
        conn.close()