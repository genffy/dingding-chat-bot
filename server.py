import hmac
import hashlib
import base64
import json
import tornado.web
import tornado.log
import logging
from defchat import DefChat
from ding import DingDing
from settings import DINGDINF_APP_SECRET, CHATGTP_EMAIL, CHATGTP_PASSWORD, DINGDING_APP_KEY, PROXY_URL
from tornado.options import define, options
define('port', default=8080, help='default port', type=int)
options.log_file_prefix = "logs/tornado_main.log"
options.log_rotate_mode = "time"    # 轮询模式: time or size
options.log_rotate_when = "D"       # 单位: S / M / H / D / W0 - W6
options.log_rotate_interval = 60    # 间隔: 60秒

class LogFormatter(tornado.log.LogFormatter):
    def __init__(self):
        super(LogFormatter, self).__init__(
            fmt='[%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

class Health(tornado.web.RequestHandler):
    def get(self):
        return self.write("ok")

class Robot(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs) -> None:
        super().__init__(application, request, **kwargs)
        self.chat = DefChat(CHATGTP_EMAIL, CHATGTP_PASSWORD, PROXY_URL)
        self.dingding = DingDing(DINGDING_APP_KEY, DINGDINF_APP_SECRET)

    async def post(self):
        timestamp = self.request.headers.get('timestamp', None)
        sign = self.request.headers.get('sign', None)
        app_secret = DINGDINF_APP_SECRET
        app_secret_enc = app_secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, app_secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(app_secret_enc, string_to_sign_enc,
                             digestmod=hashlib.sha256).digest()
        my_sign = base64.b64encode(hmac_code).decode('utf-8')
        logging.info("sign %s,  my_sign %s", sign, my_sign)
        if sign != my_sign:
            return self.finish({"errcode": 1, "msg": "签名有误"})
        data = json.loads(self.request.body)
        text = data['text']["content"]
        atUsers = data.get("atUsers", None)
        uid = data.get("senderStaffId", None)
        conversationType = data.get("conversationType", 1) # 1：单聊 2：群聊
        sessionWebhook = data.get("sessionWebhook", None)
        senderNick = data.get("senderNick", None)
        logging.info("get data from dingding %s", data)
        # 执行查询，返回消息
        msg = self.chat.ask(text)
        # msg = "你刚刚提问的是："+text
        if conversationType == "2" :
            # TODO hightlight
            self.dingding.send_user(atUsers[0]['dingtalkId'], "@{} {}".format(senderNick, msg), sessionWebhook)
        elif conversationType == "1":
            self.dingding.send_message(uid, msg)
        return self.finish({"errcode": 0, "msg": text})

urlpatterns = [
    (r"/robot_chat/", Robot),
    (r"/@in/api/health", Health)
]

# 创建Tornado实例
application = tornado.web.Application(urlpatterns, debug=True)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    [i.setFormatter(LogFormatter()) for i in logging.getLogger().handlers]
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
