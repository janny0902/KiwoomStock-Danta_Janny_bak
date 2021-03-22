from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kiwoomAPI import KiwoomAPI


def on_receive_opt10080(kw: 'KiwoomAPI', rqname, trcode):
   

    data_cnt = kw.get_repeat_cnt(trcode, rqname)
    ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}

    for i in range(data_cnt):
        date = kw.comm_get_data(trcode, "", rqname, i, "체결시간")
        open = kw.comm_get_data(trcode, "", rqname, i, "시가")
        high = kw.comm_get_data(trcode, "", rqname, i, "고가")
        low = kw.comm_get_data(trcode, "", rqname, i, "저가")
        close = kw.comm_get_data(trcode, "", rqname, i, "현재가")
        volume = kw.comm_get_data(trcode, "", rqname, i, "거래량")

        ohlcv['date'].append(date)
        ohlcv['open'].append(abs(int(open)))
        ohlcv['high'].append(abs(int(high)))
        ohlcv['low'].append(abs(int(low)))
        ohlcv['close'].append(abs(int(close)))
        ohlcv['volume'].append(int(volume))

    return ohlcv


def on_receive_opt10081(kw: 'KiwoomAPI', rqname, trcode):
    

    data_cnt = kw.get_repeat_cnt(trcode, rqname)
    ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}

    for i in range(data_cnt):
        date = kw.comm_get_data(trcode, "", rqname, i, "일자")
        open = kw.comm_get_data(trcode, "", rqname, i, "시가")
        high = kw.comm_get_data(trcode, "", rqname, i, "고가")
        low = kw.comm_get_data(trcode, "", rqname, i, "저가")
        close = kw.comm_get_data(trcode, "", rqname, i, "현재가")
        volume = kw.comm_get_data(trcode, "", rqname, i, "거래량")

        ohlcv['date'].append(date)
        ohlcv['open'].append(int(open))
        ohlcv['high'].append(int(high))
        ohlcv['low'].append(int(low))
        ohlcv['close'].append(int(close))
        ohlcv['volume'].append(int(volume))

    return ohlcv