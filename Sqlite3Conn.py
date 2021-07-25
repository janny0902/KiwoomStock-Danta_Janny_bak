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

    ##--------------------조회 기능--------------------------
    def SQL_StockListSelect(self,tableNm):  #전체리스트
        #회원 조회하기
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + tableNm ) 
        rows = cur.fetchall()

        StockList=[] 
        count=0

        for row in rows:  
            StockList.insert(count,row) 
            count+=1

        conn.close()
        return StockList

    def SQL_StockList_0(self,tableNm,StateCode): #매수전 리스트
            #회원 조회하기
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT * FROM " + tableNm +" WHERE STATE = '"+StateCode+"'") 
        rows = cur.fetchall()

        StockList=[] 
        count=0

        for row in rows:  
            StockList.insert(count,row) 
            count+=1

        conn.close()
        return StockList
