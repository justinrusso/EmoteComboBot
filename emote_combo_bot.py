import argparse
import asyncio
import json
import logging
import requests
import sys
from bot import ComboBot
from emotes import get_emotes
from logging import critical, error, info, warning, debug
from store import Store


def parse_arguments():
    """Read arguments from a command line."""
    parser = argparse.ArgumentParser(
        description='Arguments get parsed via --commands')
    parser.add_argument('-v', metavar='verbosity', type=int, default=2,
                        help='Verbosity of logging: 0 -critical, 1- error, 2 -warning, 3 -info, 4 -debug')

    args = parser.parse_args()
    verbose = {0: logging.CRITICAL, 1: logging.ERROR,
               2: logging.WARNING, 3: logging.INFO, 4: logging.DEBUG}
    logging.basicConfig(format='%(message)s',
                        level=verbose[args.v], stream=sys.stdout)

    return args


def get_channel_id(channel_name: str, config: dict[str, any]) -> str:
    headers = {'Authorization': f'Bearer {config["oauth"]}',
               'Client-Id': config["client_id"]}
    response = requests.get(
        f'https://api.twitch.tv/helix/users?login={channel_name}', headers=headers)
    data = response.json()

    if len(data) != 1:
        raise Exception('Failed to find channel')

    return data['data'][0]['id']


def main():
    config = None
    with open("config.json") as f:
        config = json.loads(f.read())

    if config is None:
        critical('No config found. Exiting')
        return

    channel_id = get_channel_id(config['channel'], {
                                "oauth": config['accessToken'], "client_id": config['clientId']})
    emotes = get_emotes(config['channel'], channel_id)

    bot = ComboBot(config['botName'],
                   f'oauth:{config["accessToken"]}', config['channel'], channel_id, emotes, Store('record.json'))
    bot.run()


if __name__ == '__main__':
    args = parse_arguments()
    main()
