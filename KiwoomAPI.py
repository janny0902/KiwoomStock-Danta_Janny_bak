from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import win32gui
import win32con 
import win32api
import Sqlite3Conn


TR_REQ_TIME_INTERVAL = 0.3

class KiwoomAPI(QAxWidget):
    def __init__ (self):
        super().__init__()
        self.output_list = []
        self.ret_data = {}
        self.set_kiwoom_api()
        self.set_event_slot()
        self.sqlConn = Sqlite3Conn.SQL_CONNECT()  ##DB

        user = self.sqlConn.SQL_UserSelect('USER') 
        self.userName = user[1].strip()
        self.accNum = user[2].strip()
        print( self.accNum)
        self.passId = user[3].strip()
        self.passAcc = user[4].strip()
        self.userId = user[6].strip()
        self.passAccNum = user[7].strip()
        

# ========== #
    def set_kiwoom_api(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def set_event_slot(self):
        # 공통
        self.OnReceiveMsg.connect(self.E_OnReceiveMsg)

        # 로그인 버전처리
        self.OnReceiveTrData.connect(self._receive_tr_data) 
        self.OnEventConnect.connect(self.E_OnEventConnect)
        self.OnReceiveTrData.connect(self.E_OnReceiveTrData)
        
        

        

# ========== #
    ### Event 함수 ###
    ## 공통 ##
    def E_OnReceiveMsg(self, sScrNo, sRQName, sTrCode, sMsg):
        print(sScrNo, sRQName, sTrCode, sMsg)

    ## 로그인 버전처리 ##
    def E_OnEventConnect(self, nErrCode):
        print(nErrCode)

        self.login_event_loop.exit()

# ========== #
    ### OpenAPI 함수 ###
    ## 로그인 버전처리 ##
    # 로그인
    def CommConnect(self):
        self.dynamicCall('CommConnect()')
        self.event_loop_CommConnect = QEventLoop()
        self.event_loop_CommConnect.exec_()

    #### 로그인 상태 확인 함수
    def GetConnectState(self):
        ret = self.dynamicCall('GetConnectState()')

        print(ret)

    #### 자동 로그인 구현
    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        print("수동 로그인 함수 호출")
        
        self.wait_secs("로그인시도", 3)
        hwnd = self.find_window("Open API Login")
        edit_id = win32gui.GetDlgItem(hwnd, 0x3E8)
        edit_pass = win32gui.GetDlgItem(hwnd, 0x3E9)
        edit_cert = win32gui.GetDlgItem(hwnd, 0x3EA)
        button = win32gui.GetDlgItem(hwnd, 0x1)
        
        self.enter_keys(edit_id, self.userId)
        self.enter_keys(edit_pass, self.passId)
        self.enter_keys(edit_cert, self.passAcc)
        self.click_button(button)
        self.click_button(button)
        self.login_event_loop.exec_()

    #### 로그인 정보 조회 함수
    def GetLoginInfo(self, kind=''):
        ret = self.dynamicCall('GetLoginInfo(String)', kind)

        print(ret) 
        
    ##주문 관련
    def E_OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
        print(sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, nDataLength, sErrorCode, sMessage, sSplmMsg)

        if sRQName == 'opt10080_req':            
            self._on_receive_tr_data(sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, nDataLength, sErrorCode, sMessage, sSplmMsg)
        else:
            self.Call_TR(sTrCode, sRQName)
            
            self.event_loop_CommRqData.exit()

    ####단일 종목 요청 함수
    def CommRqData(self, sRQName, sTrCode, nPrevNext, sScreenNo):
        
        ret = self.dynamicCall('CommRqData(String, String, int, String)', sRQName, sTrCode, nPrevNext, sScreenNo)
        
        self.event_loop_CommRqData = QEventLoop()
        self.event_loop_CommRqData.exec_()   
        time.sleep(TR_REQ_TIME_INTERVAL)
        
        
    ####시간 대기 함수
    def wait_secs(self,msg, secs=10):        
        while secs > 0:
            time.sleep(1)
            print(f"{msg} waiting: {secs}")
            secs = secs - 1

    ####TR 요청 함수
    def Call_TR(self, strTrCode, sRQName):
        self.ret_data[strTrCode] = {}
        self.ret_data[strTrCode]['Data'] = {}
        
        self.ret_data[strTrCode]['TrCode'] = strTrCode


        count = self.GetRepeatCnt(strTrCode, sRQName)
        self.ret_data[strTrCode]['Count'] = count
        

        if count == 0:
            temp_list = []
            temp_dict = {}
            for output in self.output_list:
                data = self.GetCommData(strTrCode, sRQName, 0, output)
                temp_dict[output] = data

            temp_list.append(temp_dict)
            
            self.ret_data[strTrCode]['Data'] = temp_list

        if count >= 1:
            temp_list = []
            for i in range(count):
                temp_dict = {}
                for output in self.output_list:
                    data = self.GetCommData(strTrCode, sRQName, i, output)
                    temp_dict[output] = data

                temp_list.append(temp_dict)
            
            self.ret_data[strTrCode]['Data'] = temp_list

        
            
    ####화면 찾기 기능
    def find_window(self,caption):
        hwnd = win32gui.FindWindow(None, caption)
        if hwnd == 0:
            windows = self.enum_windows()
            for handle, title in windows:
                if caption in title:
                    hwnd = handle
                    break
        return hwnd

    ##화면조회의 필요
    def window_enumeration_handler(self,hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

    ####화면 반환 기능
    def enum_windows(self):
        windows = []
        win32gui.EnumWindows(self.window_enumeration_handler, windows)
        return windows
    
    ##화면 내 버튼 클릭 이벤트
    def click_button(self,btn_hwnd):
        #win32api.SendMessage(btn_hwnd, win32con.BM_CLICK, 0, 0)
        win32api.PostMessage(btn_hwnd, win32con.WM_LBUTTONDOWN, 0, 0)
        win32api.Sleep(100)
        win32api.PostMessage(btn_hwnd, win32con.WM_LBUTTONUP, 0, 0)
        win32api.Sleep(100)

    ####자동 입력 기능
    def auto_on(self):
        try:                 

            hwnd = self.find_window("계좌비밀번호")
            if hwnd != 0:
                # 비밀번호등록
                edit = win32gui.GetDlgItem(hwnd, 0xCC)
                win32gui.SendMessage(edit, win32con.WM_SETTEXT, 0, self.passAccNum)

                # 전체계좌에 등록
                win32api.Sleep(100)
                button_register_all = win32gui.GetDlgItem(hwnd, 0xD4)
                self.click_button(button_register_all)

                # 체크박스 체크 
                #checkbox = win32gui.GetDlgItem(hwnd, 0xD3)
                #checked = win32gui.SendMessage(checkbox, win32con.BM_GETCHECK)
                #if not checked:
                #    click_button(checkbox)

                self.wait_secs("계좌입력 시도", 1)
                button= win32gui.GetDlgItem(hwnd, 0x01)
                self.click_button(button)
        except Exception as e:
            print(e)   

    def _on_receive_tr_data(self, screen_no, rqname, trcode, record_name, next,
                            unused1, unused2, unused3, unused4):
        import tr_receive_handler as tr

        self.latest_tr_data = None

        if next == '2':
            self.is_tr_data_remained = True
        else:
            
            self.is_tr_data_remained = False

        if rqname == "opt10081_req":
            self.latest_tr_data = tr.on_receive_opt10081(self, rqname, trcode)
        elif rqname == "opt10080_req":
            self.latest_tr_data = tr.on_receive_opt10080(self, rqname, trcode)

        try:
            self.event_loop_CommRqData.exit() 
                    
            
        except AttributeError:            
            pass

    def get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", code,
                               real_type, field_name, index, item_name)
        return ret.strip()
  

    def enter_keys(self,hwnd, data):
        win32api.SendMessage(hwnd, win32con.EM_SETSEL, 0, -1) 
        win32api.SendMessage(hwnd, win32con.EM_REPLACESEL, 0, data) 

    def sendOrder(self, sRQName, sScreenNo, sAccNo, nOrderType,sCode,nQty,nPrice,sHogaGb,sOrgOrderNo):
          #BSTR sRQName, // 사용자 구분명
          #BSTR sScreenNo, // 화면번호
          #BSTR sAccNo,  // 계좌번호 10자리
          #LONG nOrderType,  // 주문유형 1:신규매수, 2:신규매도 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정
          #BSTR sCode, // 종목코드
          #LONG nQty,  // 주문수량
          #LONG nPrice, // 주문가격  시장가 매수시 03
          #BSTR sHogaGb,   // 거래구분(혹은 호가구분)은 아래 참고
          #BSTR sOrgOrderNo  // 원주문번호입니다. 신규주문에는 공백, 정정(취소)주문할 원주문번호를 입력합니다.     
          # [거래구분]
          #00 : 지정가
          #03 : 시장가
          #05 : 조건부지정가
          #06 : 최유리지정가
          #07 : 최우선지정가
          #10 : 지정가IOC
          #13 : 시장가IOC
          #16 : 최유리IOC
          #20 : 지정가FOK
          #23 : 시장가FOK
          #26 : 최유리FOK
          #61 : 장전시간외종가
          #62 : 시간외단일가매매
          #81 : 장후시간외종가

        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", [sRQName, sScreenNo, sAccNo, nOrderType, sCode, nQty, nPrice, sHogaGb,sOrgOrderNo])
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()
        

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10081_req":
            self._opt10081(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass
