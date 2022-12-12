# settings.py
import os
from dotenv import load_dotenv
load_dotenv()
# config = dotenv_values(".env")
# # 或者加一个配置，会默认覆盖已有环境变量的配置，推荐
# load_dotenv(verbose=True)

# # 或者，指定配置文件地址
# from pathlib import Path  # python3 only
# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)


# 一般的非隐秘的配置，可直接写在此处
DEBUG = True

# 读取环境变量中的配置
DINGDING_APP_KEY=os.getenv("DINGDING_APP_KEY")
DINGDINF_APP_SECRET=os.getenv("DINGDINF_APP_SECRET")

CHATGTP_EMAIL=os.getenv("CHATGTP_EMAIL")
CHATGTP_PASSWORD=os.getenv("CHATGTP_PASSWORD")

PROXY_URL=os.getenv("PROXY_URL")