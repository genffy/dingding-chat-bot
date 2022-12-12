from pychatgpt import Chat, Options

class DefChat:
    def __init__(self, email=None, password=None, proxyUrl=None) -> None:
        options = Options()
        # Track conversation
        options.track = True 
        # Use a proxy
        options.proxies = proxyUrl
        # Optionally, you can pass a file path to save the conversation
        # They're created if they don't exist
        options.chat_log = "logs/chat_log.txt"
        options.id_log = "logs/id_log.txt"
        self._options = options
        # Create a Chat object
        self._chat = Chat(email, password, options)
    def ask(self, qes=None):
        if qes:
            return self._chat.ask(qes)
        return 'please input your question'
   