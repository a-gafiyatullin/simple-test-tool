import telegram
from notification.notification import Notification


class Telegram(Notification):
    MESSAGE_MAX_LEN = 4096

    def __init__(self, loggers, token, chat_id):
        """
        Parameters
        ----------
        loggers: list
            list of loggers to send
        token: str
            telegram bot token
        chat_id: str
            personal chat id for user
        """
        Notification.__init__(self, loggers)
        self.token = token
        self.chat_id = int(chat_id)

    def _send(self, text):
        message_len = len(text)

        bot = telegram.Bot(token=self.token)
        if message_len > Telegram.MESSAGE_MAX_LEN:
            for x in range(0, message_len, Telegram.MESSAGE_MAX_LEN):
                bot.sendMessage(chat_id=self.chat_id, text=text[x:x + Telegram.MESSAGE_MAX_LEN])
        else:
            bot.sendMessage(chat_id=self.chat_id, text=text)

