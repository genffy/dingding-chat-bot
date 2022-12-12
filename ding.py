import requests
import json
from settings import DINGDING_APP_KEY, DINGDINF_APP_SECRET, CHATGTP_EMAIL, CHATGTP_PASSWORD, PROXY_URL
from defchat import DefChat

class DingDing:
    def __init__(self, appKey=None, appSecret=None) -> None:
        self._appKey = appKey
        self._appSecret = appSecret
        self._token = self.get_token()
        # 机器人webhook地址
        self._webhook = ""

    def get_token(self):
        res = requests.post(
            "https://api.dingtalk.com/v1.0/oauth2/accessToken",
            data=json.dumps({"appKey": self._appKey, "appSecret": self._appSecret}),
            headers={"Content-Type": "application/json"}
        )
        token = res.json()["accessToken"]
        return token
    # 单聊
    def send_message(self, uid, message):
        res = requests.post(
            "https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend",
            data=json.dumps({
                "robotCode": self._appKey,
                "userIds": [uid],
                "msgKey": "sampleText",
                "msgParam": '{"content":"'+message+'"}'
            }),
            headers={"Content-Type": "application/json", "x-acs-dingtalk-access-token": self._token})
        print(res.text)

    # 群聊
    def send_user(self, uid, message, _webhook):
        data = {
            "at": {
                "atUserIds": [
                    uid
                ]
            },
            "text": {
                "content": message
            },
            "msgtype": "text"
        }
        if _webhook:
            # https://oapi.dingtalk.com/robot/send?access_token=8287e47cc20c8e566bdf5690e2d1183fc150b65dcb186f6a789cf7d82214fb34
            res = requests.post(
                _webhook,
                data=json.dumps(data),
                headers={"Content-Type": "application/json"
            })
            print(res.text)
        else:
            print("i don't know")

if __name__ == '__main__':
    dingding = DingDing(DINGDING_APP_KEY, DINGDINF_APP_SECRET)
    chat = DefChat(email = CHATGTP_EMAIL, password = CHATGTP_PASSWORD, proxyUrl = PROXY_URL)
    answer = chat.ask("你好")
    # 单聊
    dingding.send_message('uid', answer)
    # 群聊
    # dingding.send_user('uid',answer)
    print(answer)
