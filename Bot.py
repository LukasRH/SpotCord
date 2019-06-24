#!/usr/bin/env python

""" TODO make explanation here """

import discord
from Spotify import Spotify
from discord.ext import commands
from Auth import BotAuth, SpotifyAuth

__author__ = "Lukas Rønsholt"
__copyright__ = ""
__credits__ = []
__license__ = "?"
__version__ = "0.0.1"
__maintainer__ = "Lukas Rønsholt"
__email__ = "lukasronsholt@gmail.com"
__status__ = "Development"


class SpotCord(commands.bot):
    def __init__(self, **options):
        super().__init__(**options)

    def run(self):
        super().run(BotAuth.token)

    async def on_ready(self):
        print(
            f"\n{'#' * 40}\n{self.user.name}\nPython version: {sys.version}\n"
            f"Discord.py version: {discord.__version__}\n{'#' * 40}")
        print('\nLogged in as:\n{0} (ID: {0.id})'.format(self.user))

        self.add_cog(Spotify)

