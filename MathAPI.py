import numpy as np
import talib.abstract as ta
import pandas_datareader as data



class MathAPI:
    def __init__(self):
        self.date = 0

        #가격에 퍼센트 가격 구하기
    def percentMius(self,per,price):  # price * per  ex 1000-(1000 * 0.02) = 980   2%감소 계산
        perc = per / 100    
        result = price - price * perc
        return result

        #등락률 구하기
    def perPrice(self,price,nowprice):  #((price / nowprice) -1) * 100 
        result = ((nowprice / price)-1)*100
        
        return result

        #거래 호가 단위 구하기  
    def hogadan(self,price):
        
        reulst = 0
        
        if int(price) <= 999:
            result = 1
        elif int(price) <= 4999:
            result = 5
        elif int(price) <= 9999:
            result = 10
        elif int(price) <= 49999:
            result = 50
        elif int(price) <= 99999:
            reulst = 100
        else:
            result = 0
        return result

    def searchMoney(self,buy_money,price):  ##구매수량 구해기
        if str(price)[0] == '-':
            price = str(price)[1:]

        print(price)
        result = buy_money / int(price)
        return round(result)-1

        #TALIB 사용 MACD 및 RSI 구하기
    def GetIndicator(self, data):
        try:
            # data.insert(0, "Date", data.index)
            # data.insert(1, "korean_name", row['korean_name'])
            # data.insert(2, "english_name", row['english_name'])
           

            
            arrOpen = np.asarray(data["open"], dtype='f8')
            arrHigh = np.asarray(data["high"], dtype='f8')
            arrLow = np.asarray(data["low"], dtype='f8')
            arrClose = np.asarray(data["close"], dtype='f8')
            arrVolume = np.asarray(data["volume"], dtype='f8')
      

            
            # 이동 평균 선
            data['SMA5'] = ta.SMA(arrClose, 5)
            data['SMA10'] = ta.SMA(arrClose, 10)
            #data['SMA15'] = ta.SMA(arrClose, 15)
            data['SMA20'] = ta.SMA(arrClose, 20)
            data['SMA60'] = ta.SMA(arrClose, 60)
            data['SMA120'] = ta.SMA(arrClose, 120)

            # 골든 크로스
            data.insert(len(data.columns), "GAP_SMA5_trade", data['SMA5'] - data['close'])
            data.insert(len(data.columns), "GAP_SMA10_SMA5", data['SMA10'] - data['SMA5'])
            data.insert(len(data.columns), "GAP_SMA60_SMA5", data['SMA60'] - data['SMA5'])
            data.insert(len(data.columns), "GAP_SMA120_SMA60", data['SMA120'] - data['SMA60'])

            data['State_SMA5_trade'] = ['LOW' if s > 0 else 'HIGH' for s in data['GAP_SMA5_trade']] 
            data['State_SMA10_SMA5'] = ['LOW' if s > 0 else 'HIGH' for s in data['GAP_SMA10_SMA5']] 
            data['State_SMA60_SMA5'] = ['LOW' if s > 0 else 'HIGH' for s in data['GAP_SMA60_SMA5']]
            data['State_SMA120_SMA60'] = ['LOW' if s > 0 else 'HIGH' for s in data['GAP_SMA120_SMA60']]

            # RSI
            data['RSI'] = ta.RSI(arrClose, 14)
           

            # MACD Indecator
            # MACD가 0선을 상향돌파하면 매수(상승국면), 하향돌파하면 매도(하향국면)
            # MACD가 시그널을 상향돌파(골든크로스)하면 매수, 하향돌파(데드크로스)하면 매도가

            # MACD < 0유지, MACD와 시그널이 골든크로스로 교차 : 하락추세에서 단기 주가 상승
            # MACD < 0유지, MACD와 시그널이 데드크로스로 교차 : 장기적으로 주가 하락
            # MACD > 0유지, MACD와 시그널이 골든크로스로 교차 : 장기적으로 주가 상승
            # MACD > 0유지, MACD와 시그널이 데드크로스로 교차 : 상승추세에서 단기 주가 하락

            # MACD
            macd, macdsignal, macdhist = ta.MACD(arrClose, 12, 26, 9)
            data['MACD'] = macd
            data['MACD_SIGNAL'] = macdsignal
            data['MACD_HIST'] = macdhist

            data.insert(len(data.columns), "MACD_OSCILLATOR", data['MACD'] - data['MACD_SIGNAL'])

            macd, macdsignal, macdhist = ta.MACD(arrClose, 37, 73, 9)
            data['MACD_37'] = macd
            data['MACD_SIGNAL_37'] = macdsignal
            data['MACD_HIST_37'] = macdhist
            data.insert(len(data.columns), "MACD_OSCILLATOR_37", data['MACD_37'] - data['MACD_SIGNAL_37'])

            data['SAR'] = ta.SAR(arrHigh , arrLow, acceleration=0.01, maximum=0.2)
            

            return data

        except Exception as ex:
            print(ex)


    
            

    
        
    