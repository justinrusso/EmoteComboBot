from emotes import get_emotes
import re
from twitchio.ext import commands


class ComboBot(commands.Bot):
    def __init__(self, bot_name: str, oauth: str, channel_name: str, channel_id: str, emotes: set[str]):
        super().__init__(token=oauth, prefix='!',
                         initial_channels=[channel_name])
        self._channel_name = channel_name
        self._channel_id = channel_id
        self._emotes = emotes

        self._chain_count = 0
        self._current_emote = None

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as {self.nick}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

        await self.handle_chain(message)

    @commands.command()
    async def refresh(self, ctx: commands.Context):
        if ctx.author.is_mod:
            self._emotes = get_emotes(self._channel_name, self._channel_id)
            await ctx.send(f'Refreshed emotes list. {len(self._emotes)} non-Twitch emotes found.')

    async def handle_chain(self, message):
        message_emotes = self.parse_emotes(message)

        if self._current_emote is None:
            if len(message_emotes) > 0:
                self._current_emote = list(message_emotes)[0]
                self._chain_count = 1
        elif len(message_emotes) > 0 and self._current_emote in message_emotes:
            self._chain_count += 1
        else:
            if self._chain_count >= 5:
                await message.channel.send(
                    f'{self._chain_count}x {self._current_emote} combo')
            self._chain_count = 0
            self._current_emote = None

            if len(message_emotes) > 0:
                self._current_emote = list(message_emotes)[0]
                self._chain_count = 1

    def parse_emotes(self, message) -> set[str]:
        message_emotes = set()
        if len(message.tags['emotes']) > 0:
            message_emotes.update(self.parse_twitch_emotes(message))

        unique_words = set(message.content.split())
        other_emotes = self._emotes.intersection(unique_words)
        message_emotes.update(other_emotes)

        return message_emotes

    def parse_twitch_emotes(self, message):
        message_twitch_emotes = set()

        emote_tags = message.tags['emotes'].split('/')

        for emote_tag in emote_tags:
            emote_tag = re.sub(r'.*:', '', emote_tag)
            # Get only the first pair of indexes of the emote - we dont need more than that
            [start, end] = [int(index)
                            for index in emote_tag.split(',')[0].split('-')]
            emote_text = message.content[start:end + 1]
            message_twitch_emotes.add(emote_text)
        return message_twitch_emotes
