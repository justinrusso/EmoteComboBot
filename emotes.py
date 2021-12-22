import requests
from logging import critical, error, info, warning, debug


def get_ffz_emotes(channel_name: str):
    """
    Gets the global and channel emotes for FFZ
    """
    emotes = set()

    response = requests.get(
        f'https://api.frankerfacez.com/v1/room/{channel_name}')

    if response.ok is False:
        return emotes

    data = response.json()

    for emote_set in data['sets'].values():
        for emote in emote_set['emoticons']:
            emotes.add(emote['name'])

    response = requests.get(f'https://api.frankerfacez.com/v1/set/global')
    data = response.json()
    for emote_set in data['sets'].values():
        for emote in emote_set['emoticons']:
            emotes.add(emote['name'])
    return emotes


def get_bttv_emotes(channel_id: str):
    """
    Gets the global and channel emotes for BTTV
    """
    emotes = set()

    response = requests.get(
        f'https://api.betterttv.net/3/cached/users/twitch/{channel_id}')

    if response.ok is False:
        return emotes

    data = response.json()
    for emote in data['channelEmotes']:
        emotes.add(emote['code'])
    for emote in data['sharedEmotes']:
        emotes.add(emote['code'])

    response = requests.get(
        f'https://api.betterttv.net/3/cached/emotes/global')
    data = response.json()
    for emote in data:
        emotes.add(emote['code'])

    return emotes


def get_7tv_emotes(channel_name: str):
    """
    Gets the global and channel emotes for 7TV
    """
    emotes = set()

    response = requests.get(
        f'https://api.7tv.app/v2/users/{channel_name}/emotes')

    if response.ok is False:
        return emotes

    data = response.json()
    for emote in data:
        emotes.add(emote['name'])

    response = requests.get(f'https://api.7tv.app/v2/emotes/global')
    data = response.json()
    for emote in data:
        emotes.add(emote['name'])

    return emotes


def get_emotes(channel_name: str, channel_id: str):
    info('Loading emotes...')

    emotes = set()
    emotes.update(get_ffz_emotes(channel_name))
    emotes.update(get_bttv_emotes(channel_id))
    emotes.update(get_7tv_emotes(channel_name))

    info(f'Successfully loaded {len(emotes)} emotes.')

    return emotes
