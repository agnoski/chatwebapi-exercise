class Message:
    def __init__(self, chat_code, user_code, user_name, line, text):
        self.chat_code = chat_code
        self.user_code = user_code
        self.user_name = user_name
        self.line = line
        self.text = text