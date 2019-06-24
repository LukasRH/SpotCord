#!/usr/bin/env python

""" Authentication credentials for discord and sporify, spesified by environment variables """

import os
import sys

__author__ = "Lukas Rønsholt"
__license__ = "MIT"
__version__ = "0.0.1"
__status__ = "Development"


class BotAuth(object):
    try:
        token = os.environ['BOT_TOKEN']
        prefix = os.environ['BOT_PREFIX']
    except KeyError as e:
        print(f"Missing environment variable {e.args[0]}")
        sys.exit(0)


class SpotifyAuth(object):
    try:
        scope = "playlist-modify-public user-modify-playback-state user-read-playback-state"
        client_id = os.environ['BOT_TOKEN']
        client_secret = os.environ['BOT_TOKEN']
        redirect_uri = "http://localhost/"
    except KeyError as e:
        print(f"Missing environment variable {e.args[0]}")
        sys.exit(0)