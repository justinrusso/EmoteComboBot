from emotes import get_emotes
from python_twitch_irc import TwitchIrc

# Simple echo bot.


class ComboBot(TwitchIrc):
    def __init__(self, bot_name: str, oauth: str, channel_name: str, channel_id: str, emotes: set[str]):
        super.__init__(bot_name, oauth)
        self._channel_name = channel_name
        self._channel_id = channel_id
        self._emotes = emotes

    def on_connect(self):
        self.join(f'#{self._channel_name}')

    # Override from base class
    def on_message(self, timestamp, tags, channel, user, message: str):
        print(tags, user, message)
        if message.lower() == '!refresh':
            self._emotes = get_emotes(self._channel_name, self._channel_id)
