# Emote Combo Bot

Emote Combo Bot is a Twitch chat bot that tracks the amount of the same emote found in successive emotes in a row in a chat channel. The bot supports emotes from Twitch, BTTV, FFZ, and 7TV.

## Commands 

- Typing `!combo` in chat will output the largest combo chain.
- Typing `!refresh` allows moderators of the channel to refresh the emotes from BTTV, FFZ, and 7TV to ensure the emotes are up to date.

## Running the bot

1. Create a copy of `config.example.json` and name it `config.json`. Set up the configuration file as necessary.
2. Install dependencies using `pip install -r requirements.txt`
3. Run the bot with `python bot.py`
