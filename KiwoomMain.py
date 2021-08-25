import sys
from PyQt5.QtWidgets import *

import FinanceDataReader as fdr

from Config import *
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *
from PyQt5 import QtTest
import KiwoomAPI
import MathAPI
import pandas as pd
import schedule
import time
import Sqlite3Conn
import TelegramAPI
#pip install python-telegram-bot --upgrade
#pip install --upgrade pip
        



class KiwoonMain:   
        

    def __init__(self):
        
        self.kiwoom = KiwoomAPI.KiwoomAPI()
        #self.kiwoom.CommConnect()        
        self.mathsub = MathAPI.MathAPI()                    
        self.telegram = TelegramAPI.TelegramAPI()
        self.kiwoom.comm_connect()  ##자동로그인 
        self.flag = True
        self.sqlConn = Sqlite3Conn.SQL_CONNECT()  ##DB

# ========== #
    def GetLoginInfo(self):
        # 로그인 상태
        self.kiwoom.GetConnectState()

        # 로그인 정보
        self.kiwoom.GetLoginInfo("ACCOUNT_CNT")
        self.kiwoom.GetLoginInfo("ACCLIST")
        self.kiwoom.GetLoginInfo("USER_ID")
        self.kiwoom.GetLoginInfo("USER_NAME")
        self.kiwoom.GetLoginInfo("KEY_BSECGB")
        self.kiwoom.GetLoginInfo("FIREW_SECGB")
        self.kiwoom.GetLoginInfo("GetServerGubun")

    def myAccount(self):
        self.kiwoom.output_list = output_list['OPW00018']        
        self.kiwoom.SetInputValue("계좌번호"	,  self.kiwoom.accNum)
        self.kiwoom.SetInputValue("비밀번호"	,   self.kiwoom.passAcc)
          
        self.kiwoom.SetInputValue("비밀번호입력매체구분"	,  "00")
        self.kiwoom.SetInputValue("조회구분"	,  "2")
        QTimer.singleShot(2 * 1000, self.kiwoom.auto_on)
        self.kiwoom.dynamicCall("KOA_Functions(QString, QString)", "ShowAccountWindow", "")
        self.kiwoom.wait_secs("계좌입력 시도", 1)
        
      
    def myAccountSh(self): ## 계좌 조회
        #TODO 3. (좌니) 잔고조회 (현재 잔고 조회해서 보유종목및 수익률 확인 ) (완료)        
        self.kiwoom.output_list = output_list['OPW00018']  
        print(self.kiwoom.accNum)
        self.kiwoom.SetInputValue("계좌번호"	,  self.kiwoom.accNum)
        self.kiwoom.SetInputValue("비밀번호"	,   self.kiwoom.passAcc)
          
        self.kiwoom.SetInputValue("비밀번호입력매체구분"	,  "00")
        self.kiwoom.SetInputValue("조회구분"	,  "2")
        self.kiwoom.CommRqData( "RQName0"    ,  "opw00018"	,  "0"	,  "0391"); 
        
        result =  self.kiwoom.ret_data['opw00018']    
        
        ##result 사용법
        #for stock in result['Data']:
        #    print('----------------')
            
        #    print('종목번호',stock['종목번호'])
        #    print('종목명',stock['종목명'])
        #    print('보유수량',stock['보유수량'])
        #    print('수익률',stock['수익률(%)'])
        #    print('현재가',stock['현재가'])
        #    print('매입가',stock['매입가'])    
        return result 
    def OPT10001(self,scode):   #단일 종목 검색
        
        self.kiwoom.output_list = output_list['OPT10001']
        self.kiwoom.SetInputValue("종목코드", scode)
        self.kiwoom.CommRqData("OPT10001", "OPT10001", 0, "0101")
        
        return self.kiwoom.ret_data['OPT10001']    

    def run(self):
        
        ## 스케줄러 돌리기전 기본 시작 기능들 (로그인,계좌입력 등 기능)
        result = api_con.GetLoginInfo()  #로그인( TODO 자동으로 변경 필요)
        api_con.myAccount()              #계좌입력(자동 완성)        
        #print('program end')

        #self.stockSearch()
        self.kiwoom.GetConditionLoad()
        self.kiwoom.SendCondition("0101", "삼프로단타띄기", 33, 0)  
        print('program running...')
        msg_String = "program running..."
        self.telegram.Tel_MsgPush(msg_String)   
        ####------------------------####
        #전체 스토리
        #0850 스케줄 작동 로그인 기능 실행
        #0900~0910 첫 종목 선발 및 시가 확인(두 종목 대상)
        #0910~0300 단타 시작 (25초 단위로 거래 판단 2종목)
        #0300~0315 당일 전체 매도 (상한가 종목 제외)  
        # 
        #1800 : 당일 손익 계산 결과 통보
        #매도못한 종목 손익 확인
        #       




        #### 주식 단타 프로그램 가이드 ####
        #### 중요!!! 개발 참여 3인 외 다른 사람에게 코드 공유 절대금지!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!------집중
        #### 모르는건 일단 구글검색  : 파이썬 키움주식 *** (EX:잔고조회, 매수기능,매도기능, 실시간검색 순위) 이런식으로 치면 거의 나옴.
        #### TODO 읽고 할 수 있는부분 또는 하고싶은 부분 만들면됨  TODO 뒤에 본인 이름적고 커밋 하셈 안건들겠음  .
        #### 완성 못해도 상관없으니 그냥 해보셈
        
        #### 기능 구현 위치는 TODO 아래에 그냥 만들면됨

        #### KiwoomMain.py - 실행 요소만 모아놓아야함
        #### KiwoomAPI.py - KOAStudioSA 에서 제공해주는 기능 메소드 구현시 여기에 작성
        
        

        #TODO 1. (정세현) 스케줄러 적용  구글에 python 스케줄러 라고 검색하면  사용 방법 나옴  10초에 한번식 print('성공') 찍는 기능 만들기
                    #매일 오후 3시 15분에 print('매도') 찍기 기능  
        def job():
            self.nowdate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            #print('매도')
            ### TODO 정세현 조건 검색 결과 받아오기  ###텔레그램으로 매수 매도 상황 받을꺼면 물어보셈


            #print('종목명 프린트')
            ###-------------------------- 검색 결과 받아오기끝
            #self.kiwoom.SendCondition("0101", "초단타", 0, 0)
            #item = self.kiwoom.serchItem()
            #print(item)

            ###TODO 정세현 조건검색 결과 DB 추가 (상태 확인 컬럼 넣고  0:매수전 상태  1:매수상태  2:매도상태)
            

            #(주완) STOCK_LIST 테이블 정보
            # S_NUM : 종목번호
            # S_NAME : 종목이름
            # S_PRICE : 현재가
            # B_PRICE : 매입가
            # H_PRICE : 최고가
            # B_TIME : 구매시간
            # E_TIME : 판매시간
            # STATE : 상태
            # EA    : 매수 수량 INTEGER
            
            #print('종목 DB 추가 완료 메시지 ')
            ###-------------------------- DB 추가 끝
            StockList = self.sqlConn.SQL_StockList('STOCK_LIST','1') 
            #Sprice = StockList[0][2]
            #print('------- 종목명 -------')
            #for stock in StockList:
            ##    print(stock[1])
            #    print(stock[2])
            #    print(stock[3])

                     

            ###TODO DB 읽어서 종목 리스트 뿌리기 (0: 매수전 상태 리스트)
            ###매수 기능을 실행,  
            
            #print("#####")
           
            StockList_0 = self.sqlConn.SQL_StockList('STOCK_LIST','0') 
            #print(StockList_0)
            #print("-------------")
            if len(StockList_0) >= 1:
                for stock in StockList_0:
                    result = self.OPT10001(stock[0])
                    #print(result)
                    #print(result['Data'][0]['현재가'],'현재가') 
                    NowPrice = result['Data'][0]['현재가'].strip()
                    if  NowPrice[0] ==  '-':
                        NowPrice = NowPrice[1:]
                    S_name = result['Data'][0]['종목명'].strip()
                    S_price = NowPrice
                    B_price = NowPrice
                    H_price = NowPrice
                    S_num = result['Data'][0]['종목코드'].strip()
                    #print(S_num,'종목코드')
                    #print(B_price,'매수가')
                    #print(self.kiwoom.buyMoney,'매수한도금액')
                    
                    BuyMoneyMax = self.kiwoom.buyMoney
                    EA = self.mathsub.searchMoney(int(BuyMoneyMax),int(B_price))
                    self.kiwoom.output_list = output_list['OPW00005']        
                    self.kiwoom.SetInputValue("계좌번호"	,  self.kiwoom.accNum)
                    self.kiwoom.SetInputValue("비밀번호"	,  self.kiwoom.passAcc)     
                    self.kiwoom.SetInputValue("비밀번호입력매체구분"	,  "00")
                    self.kiwoom.CommRqData( "RQName"	,  "OPW00005"	,  "0"	,  "0391")
                    result_BOX =  self.kiwoom.ret_data['OPW00005']  
                    #print(result_BOX)

                    #잠시막음
                    self.kiwoom.sendOrder("시장가_매수", "0101", self.kiwoom.accNum, 1, S_num ,EA,0,"03","")
                    self.kiwoom.wait_secs("매수", 0.5)
                    print(self.nowdate , '매수 시점')
                    msg_String = "종목코드:%s\n종목명:%s\n매수가:%s \n시장가 매수" %(stock[0],S_name,S_price)
                    print(msg_String)
                    self.telegram.Tel_MsgPush(msg_String)  
                    self.sqlConn.SQL_UPDATE_F("UPDATE STOCK_LIST SET S_NAME=?, S_PRICE = ?,B_PRICE=?,H_PRICE=?,B_TIME=?,E_TIME=?, STATE = 1 ,EA=?  WHERE S_NUM=?",(S_name,S_price,B_price,H_price,0000,0000,EA,S_num))
            
            #item = self.kiwoom.serchItem()
            #print('매수전 상태 종목 리스트')
            ###-------------------------- 매수전 리스트 뿌리기 끝

            ### TODO 매수상태 종목 뿌리기 (1:매수 상태)

            #print('매수상태 종목 뿌리기 끝')
            ###--------------------------- 매수상태 종목 뿌리기

            ### TODO 매수 기능 매도 기능  만들기
            ### 시나리오 : 1. 매수전 리스트 불러와서 매수 기능 실행 (0:매수전  > 1:매수상태  상태값 변경, 2:매도)    --MYSQL UPDATE 검색해보셈
            ###           2. 매수전 종목이 없으면 무시

            
            ###           3. 매수상태 리스트 불러와서 현재가 VS 최고가 비교, 갱신
            ###           3_1. 매수가 -1%시 매도 (손절가)
            ###           4. 최고가 VS 현재가 비교시 -1% 이면 매도            
            ###           5. 매도 진행시 잔고 테이블에 수익률 매수가격 매도가격  시간  등등 입력 (일지 확인용)
            # 3. 현재가 vs 최고가 비교, 갱신
            StockList = self.sqlConn.SQL_StockList('STOCK_LIST','1') 
            for stock in StockList:
                    result = self.OPT10001(stock[0])
                    #print(result)
                    #print(result['Data'][0]['현재가'],'현재가') 
                    NowPrice = result['Data'][0]['현재가'].strip()
                    if  NowPrice[0] ==  '-':
                        NowPrice = NowPrice[1:]
                   
                    S_price = int(NowPrice)
                    
                    H_price = stock[4]
                    if H_price < S_price:   #고가 보다 현재가가 높으면 고가를 현재가로 갱신
                        H_price = S_price

                    S_num = result['Data'][0]['종목코드'].strip()
                    #print(S_num,'종목코드')
                    
                    
                    self.sqlConn.SQL_UPDATE_F("UPDATE STOCK_LIST SET S_PRICE=?,H_PRICE=? WHERE S_NUM=?",(S_price,H_price,S_num))
            
            #print('------- 종목명 -------')
            for stock in StockList:
                snum = stock[0]
                snam = stock[1]
                B_price = stock[3]
                NowPrice = result['Data'][0]['현재가'].strip()
                if  NowPrice[0] ==  '-':
                    NowPrice = NowPrice[1:]
                S_price = int(NowPrice)  
                H_price = stock[4]
                EA = stock[8]
                perprice = self.mathsub.percentMius(1,H_price)                
                #print(S_price,'현재가')
                #print(H_price,'최고가')
                #print(perprice,'익절가')

                if S_price < perprice:
                    print(self.nowdate , '익절매도 시점')
                    self.kiwoom.sendOrder("시장가_매도", "0101", self.kiwoom.accNum, 2, snum,EA,0,"03","")
                    self.kiwoom.wait_secs("매도", 0.5) 
                    self.sqlConn.SQL_UPDATE_F("UPDATE STOCK_LIST SET  STATE=2 WHERE S_NUM=?",(S_num,))
                    #수정필요
                    msg_String = "종목코드:%s\n종목명:%s\n매수가:%s\n매도가:%s\n 최고가 -2 퍼센 매도(익절)" %(snum,snam,str(B_price),str(S_price))
                    print(msg_String)
                    self.telegram.Tel_MsgPush(msg_String)  

            print(self.nowdate,'매수 매도 기능 끝')


            # 3_1. 매수가 -1%시 매도 (손절가) (완료,매도기능 추가필요)            
            StockList = self.sqlConn.SQL_StockList('STOCK_LIST','1')
            #print('------- 종목명 -------')
            for stock in StockList:
                snum = stock[0]
                S_price = stock[2]   
                B_price = stock[3]
                EA = stock[8]
                perprice = self.mathsub.percentMius(1,B_price)
                #print(S_price,'현재가')
                #print(B_price,'매수가')
                #print(perprice,'손절가')

                if S_price < perprice:
                    print(self.nowdate , '손절매도')
                    self.kiwoom.sendOrder("시장가_매도", "0101", self.kiwoom.accNum, 2, snum ,EA,0,"03","")
                    self.kiwoom.wait_secs("매도", 0.5)  
                    self.sqlConn.SQL_UPDATE_F("UPDATE STOCK_LIST SET  STATE=2 WHERE S_NUM=?",(S_num,))
                    msg_String = "종목코드:%s\n종목명:%s\n매수가:%s\n매도가:%s\n 1퍼센 손절 매도" %(snum,snam,B_price,S_price)
                    self.telegram.Tel_MsgPush(msg_String)            
                    print(msg_String)

            #print('매수 매도 기능 끝')
            ###-------------------------- 매수 매도 기능 작업 끝

            ### TODO 3시이후 장마감후 금일 수익률 텔레그램으로 전송

            ###----------------수익률 관리 끝

            ### TODO 블로그 게시물 작성(좌니)
            ###-----------------끝
            



        


            #print('테스트')
            #OPT10030  당일 거래량 상위 요청
            ##시장구분 = 000:전체, 001:코스피, 101:코스닥
            ##관리종목포함 = 0:관리종목 미포함, 1:관리종목 포함
            ##정렬구분 = 1:거래량, 2:거래회전율, 3:거래대금
            #self.kiwoom.output_list = output_list['OPT10030']        
            #self.kiwoom.SetInputValue("시장구분"	,  '000')
            #self.kiwoom.SetInputValue("정렬구분"	,  "1")
            #self.kiwoom.SetInputValue("관리종목포함"	,   '14')        
            #self.kiwoom.CommRqData( "RQName"    ,  "OPT10030"	,  "0"	,  "0101")
            
            
            #result_Toplist =  self.kiwoom.ret_data['OPT10030']    
            #print(result_Toplist['Data'][0])   #1위
            #print(result_Toplist['Data'][1])   #2위
            #print(result_Toplist['Data'])
            #print("---------------------")
            
            #OPT10032 거래대금 상위 요청

            #print("test1")
            #self.kiwoom.output_list = output_list['OPT10065'] 
            #OPT10065 장중투자자별 매매상위요청
            #매매구분 = 1:순매수, 2:순매도
            #self.kiwoom.SetInputValue("매매구분","1")
            #시장구분 = 000:전체, 001:코스피, 101:코스닥    
            #self.kiwoom.SetInputValue("시장구분",  "000")
            #기관구분 = 9000:외국인, 9100:외국계, 1000:금융투자, 3000:투신, 5000:기타금융, 4000:은행, 2000:보험, 6000:연기금, 7000:국가, 7100:기타법인, 9999:기관계
            #self.kiwoom.SetInputValue("기관구분",  "9000")
            
            #self.kiwoom.CommRqData( "RQName1"    ,  "OPT10065",  "0"	,  "0101")
            #result_marketTop =  self.kiwoom.ret_data['OPT10065']
            #print(result_marketTop)
            #print("----------------------") 
            
            
            #opt90003  프로그램순매수 상위50 요청           
            #매매상위구분 = 1:순매도상위, 2:순매수상위
            #print('test2')
            #self.kiwoom.output_list = output_list['OPT90003'] 
            #self.kiwoom.SetInputValue("매매상위구분"	,  "2")
            #금액수량구분 = 1:금액, 2:수량
            #self.kiwoom.SetInputValue("금액수량구분"	,  "1")
            #시장구분 = P00101:코스피, P10102:코스닥
            #self.kiwoom.SetInputValue("시장구분"	,  "P00101")
            
            #self.kiwoom.CommRqData( "RQName2"    ,  "OPT90003"	,  "0"	,  "0101")
            #result_Program_1 =  self.kiwoom.ret_data['OPT90003']

            #self.kiwoom.SetInputValue("매매상위구분"	,  "2")
            #금액수량구분 = 1:금액, 2:수량
            #self.kiwoom.SetInputValue("금액수량구분"	,  "1")
            #시장구분 = P00101:코스피, P10102:코스닥
            #self.kiwoom.SetInputValue("시장구분"	,  "P10102")
            
            #self.kiwoom.CommRqData( "RQName3"    ,  "OPT90003"	,  "0"	,  "0101")
            #result_Program_2 =  self.kiwoom.ret_data['OPT90003']

            #print(result_Program_1)
            #print(result_Program_2)

            #print("--------------------")


            #TODO 1-3-1. (정세현) 키움종목 매수 기능 -조건 설정  talib 이용
                        #5분봉 기준 20일선 골드 크로스 매수  

            #TODO 2-1. (윤학) 키움 종목 매수 (한개 종목 코드를 입력하면 해당 종목 매수 기능 ) 
            ##sendOrder API 확인 : KiwoomAPI에있음
            
           
            #TODO 2-2-1 (좌니) 키움 종목 매도 기능 - 조건 설정  
                        # 5선 데드크로스 + 호가 호가단위 3칸 이상 넘으면 매도, (손절)(완료)
            
            #result  = self.myAccountSh()   
            #for stock in result['Data']:
            #   if stock['수익률(%)'][0] =='-':
            #      if int(stock['수익률(%)'][-4])>=1:
            #         hoga = self.mathsub.hogadan(stock['현재가'])
                #        print(hoga, '호가')  ##호가 4계단 밑에 갈시 손절!  
                #       print(stock['종목명'])
                ##      print(stock['수익률(%)'])
                    #    print("-1% 손해시 매도!")

                        # 5분봉기준 전봉 거래량 기준 60% 이상 하락시 매도, (익절)(좀더 파악)
                        
            # 5분봉기준 5일선 데드크로스시 매도(완료)
            ##데이터 수신 
            #fdr = naver stock 데이터
            #df = fdr.DataReader('005930')
            #df = df.rename(columns=lambda col:col.lower())           
        
            #data = self.mathsub.GetIndicator(df)
            #print(data)     ##일봉 데이터
            #self.kiwoom.output_list = output_list['OPT10080'] 

            #self.kiwoom.SetInputValue("종목코드",  "005930")
            #self.kiwoom.SetInputValue("틱범위",   "3")
            #self.kiwoom.SetInputValue("수정주가구분	"	,   "1")        
            #self.kiwoom.CommRqData("opt10080_req", "OPT10080", 0, "0101")
            #ohlcv = self.kiwoom.latest_tr_data

            
            #data_min = pd.DataFrame.from_dict(ohlcv)
            #data_min.sort_values(by=['date'], axis=0, inplace=True)  #data_min 역순 정렬  최근데이터 하단으로
        
            #data_min = self.mathsub.GetIndicator(data_min)
            #print(data_min)   ##분봉데이터



            #print(data_min.iloc[-1]['date'])   -1은 현재봉 값변화중 
            #print(data_min.iloc[-1]['SMA5']) 
            #print(data_min.iloc[-1]['close'])
            #if int(data_min.iloc[-1]['close']) < int(data_min.iloc[-1]['SMA5']):
            #    print("5일선 데드크로스 매도!") 
            #print(data_min.iloc[-1]['SMA10'])
            #print(data_min.iloc[-1]['SMA20'])

            
            
            

            #TODO 4. (좌니) 다음날 매수 종목 미리 서칭 기능(거래량 , 상승률, 뉴스 등 포함) 
            #print(self.kiwoom.ret_data.keys())
            #print(self.kiwoom.ret_data['OPT90003'])
            #print("program end")

        def flagfun():
            self.flag= False

        def stockSearch():
            self.kiwoom.GetConditionLoad()
            self.kiwoom.SendCondition("0101", "삼프로단타띄기", 33, 0)  

        def checkProgram():
            print('program running...')
            msg_String = "program running..."
            self.telegram.Tel_MsgPush(msg_String)            


        schedule.every(10).seconds.do(job)   ##반복시간
        schedule.every(61).seconds.do(stockSearch)   ##반복시간
        schedule.every(600).seconds.do(checkProgram)  ##전체 시간
        schedule.every(18000).seconds.do(flagfun)  ##전체 시간
        #schedule.every().day.at("20:48").do(job)

        while self.flag:
            schedule.run_pending()
            
        time.sleep(1)



       

app = QApplication(sys.argv)
api_con = KiwoonMain()

api_con.run()



