from pychatgpt import Chat, Options
from settings import CHATGTP_EMAIL, CHATGTP_PASSWORD, PROXY_URL
options = Options()

# Track conversation
options.track = True 

# Use a proxy
options.proxies = PROXY_URL

# Optionally, you can pass a file path to save the conversation
# They're created if they don't exist
options.chat_log = "logs/chat_log.txt"
options.id_log = "logs/id_log.txt"

# Create a Chat object
chat = Chat(CHATGTP_EMAIL, CHATGTP_PASSWORD, options)
answer = chat.ask("How are you?")
print(answer)
