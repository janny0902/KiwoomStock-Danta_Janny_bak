import sqlite3
import time

class SQL_CONNECT:
    def __init__(self):
        self.db_path = "C:/Users/janny0902/kiwoom_danta.db"  #DB경로
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