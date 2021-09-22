import telegram

class TelegramAPI:
    def __init__(self):
        self.APICODE = "1920006088:AAGLQLxo0RlQQtK-K3LL8UO3GPcmiCHrwSA"  #DANTA_BOT
        self.BOTID = "-449307718"    #DANTA_BOT - 그룹채팅방ID
        #self.BOTID = "1431053678"    #janny_bot(좌니가족있는방)
        #self.BOTID = "1431521277"    #DANTA_BOT - 그룹채팅방ID(좌니가족있는방)


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
    
    