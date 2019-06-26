#!/usr/bin/env python

import discord
import sys
from Spotify import Spotify
from discord.ext import commands
from Auth import BotAuth

__author__ = "Lukas Rønsholt"
__license__ = "MIT"
__version__ = "0.0.1"
__status__ = "Development"


class SpotCord(commands.Bot):
    def __init__(self, **options):
        super().__init__(**options, command_prefix=BotAuth.prefix)

    def run(self):
        super().run(BotAuth.token)

    async def on_ready(self):
        print(
            f"\n{'#' * 40}\n{self.user.name}\nPython version: {sys.version}\n"
            f"Discord.py version: {discord.__version__}\n{'#' * 40}")
        print('\nLogged in as:\n{0} (ID: {0.id})'.format(self.user))

        self.add_cog(Spotify(self))

