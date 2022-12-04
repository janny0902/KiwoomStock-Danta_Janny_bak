import telegram
from MyPrivacy import *

class TelegramAPI:
    def __init__(self):
        self.APICODE = APICODE  #janny_bot
        self.BOTID = BOTID    #주식 - 그룹채팅방ID

    def Tel_GetId(self):
        #텔레그램 봇 아이디 구하기
        chat_token = self.APICODE
        chat = telegram.Bot(token = chat_token)
        updates = chat.getUpdates()
        for u in updates:
            print(u.message['chat']['id'])  ##출력 결과  janny_Bot id

    def Tel_MsgPush(self,msgString):
        telgm_token = self.APICODE #API 코드
        bot = telegram.Bot(token = telgm_token)
        text = msgString
        bot.sendMessage(chat_id = self.BOTID , text=text)

