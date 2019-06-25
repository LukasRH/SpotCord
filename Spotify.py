#!/usr/bin/env python

""" Discord bot cog for connecting to and controlling a spotify instance """

import os
import sys
from time import sleep

import spotipy.spotipy as spotipy
import spotipy.spotipy.util as util
from discord import Color
from discord.embeds import Embed
from discord.ext import commands
from Auth import SpotifyAuth
from collections import deque

__author__ = "Lukas Rønsholt"
__license__ = "MIT"
__version__ = "0.0.1"
__status__ = "Development"


class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token = self.get_spotify_token(SpotifyAuth.client_id)
        self.stdout = SpotifyAuth.stdout

        self.discord_queue = deque()
        self.spotify_queue = deque()

        if self.token:
            self.sp = spotipy.Spotify(auth=self.token)
            self._get_playlist_running()
            self.sp.trace = False
        else:
            print("Could not obtain a spotify token!")
            sys.exit(0)

    @staticmethod
    def get_spotify_token(username):
        try:
            return util.prompt_for_user_token(username, scope=SpotifyAuth.scope, client_id=SpotifyAuth.client_id,
                                              client_secret=SpotifyAuth.client_secret,
                                              redirect_uri=SpotifyAuth.redirect_uri,
                                              cache_path=os.path.join(os.getcwd(), 'cache', f'{SpotifyAuth.user_id}'))
        except AttributeError:
            os.remove(f".cache-{username}")
            return util.prompt_for_user_token(username, scope=SpotifyAuth.scope, client_id=SpotifyAuth.client_id,
                                              client_secret=SpotifyAuth.client_secret,
                                              redirect_uri=SpotifyAuth.redirect_uri,
                                              cache_path=os.path.join(os.getcwd(), 'cache', f'{SpotifyAuth.user_id}'))

    @staticmethod
    def create_song_embed(song, title="Track Details"):
        artists = ""
        for artist in song['item']['album']['artists']:
            artists += f"{artist['name']}\n"

        embed = Embed(title=title,
                      url=song['item']['external_urls']['spotify'],
                      color=Color.green())
        embed.set_thumbnail(url=song['item']['album']['images'][1]['url'])
        embed.add_field(name="Track name:", value=song['item']['name'])
        embed.add_field(name="Artist:", value=artists)
        embed.add_field(name="Track Uri:", value=song['item']['uri'])

        return embed

    @staticmethod
    def create_track_embed(song, title="Track Details"):
        artists = ""
        for artist in song['album']['artists']:
            artists += f"{artist['name']}\n"

        embed = Embed(title=title,
                      url=song['external_urls']['spotify'],
                      color=Color.green())
        embed.set_thumbnail(url=song['album']['images'][1]['url'])
        embed.add_field(name="Track name:", value=song['name'])
        embed.add_field(name="Artist:", value=artists)
        embed.add_field(name="Track Uri:", value=song['uri'])

        return embed

    @staticmethod
    def _combine_track_dicts(dict1, dict2):
        for track in dict2['items']:
            dict1['items'].append(track)

    def set_stdout(self, id):
        self.stdout = id

    def get_track_info(self, uri):
        return self.sp.track(uri)

    def play_song(self, uri, reset=True):
        self.sp.start_playback(uris=[uri])
        sleep(0.1)
        if reset:
            pass
            # self.reset_autoplay() TODO make autoplay
        return self.sp.current_user_playing_track()

    def play_next_song(self, reset=True):
        if len(self.discord_queue) != 0:
            song = self.play_song(self.discord_queue.popleft(), reset=reset)
        elif len(self.spotify_queue) != 0:
            song = self.play_song(self.spotify_queue.popleft(), reset=reset)
        else:
            return None
        return song

    def _get_playlist_running(self):
        playback = self.sp.current_playback()
        if playback is not None and playback['context'] is not None:
            playlist_uri = playback['context']['uri']
            current_track = playback['item']['uri']
            tracks = self._get_playlist_tracks(playlist_uri)
            add = False
            for track in tracks['items']:
                if track['track']['uri'] == current_track:
                    add = True
                    continue
                if add:
                    self.spotify_queue.append(track['track']['uri'])
        else:
            print("No running spotify playlist, starting with empty playlist")

    def _get_playlist_tracks(self, playlist_uri):
        result = self.sp.playlist_tracks(playlist_uri, fields="items(track(uri)),next")
        tracks = dict(result)
        result = self.sp.next(result)
        while result is not None:
            self._combine_track_dicts(tracks, dict(result))
            result = self.sp.next(result)

        # TODO sort tracks by given parem, default no sort

        return tracks

    @commands.command(name="user")
    async def _current_user(self, ctx):
        user = self.sp.current_user()

        msg = Embed(title=f"Currently logged in Spotify user",
                    description=f"Display name:\t{user['display_name']}\n"
                    f"Followers:\t\t{user['followers']['total']}\n"
                    f"Spotify Uri:\t{user['uri']}",
                    color=Color.green(),
                    url=user['external_urls']['spotify'])

        try:
            msg.set_thumbnail(url=user['images'][0]['url'])
        except IndexError:
            pass

        await ctx.send(embed=msg)

    @commands.command(name="playing", pass_context=True)
    async def _current_playing_song(self, ctx, title="Currently Playing"):
        song = self.sp.current_user_playing_track()

        if song is not None:
            await ctx.send(embed=self.create_song_embed(song, title))
        else:
            await ctx.send(embed=Embed(title="No Song playing", color=Color.red()))

    # TODO make host/admin only
    @commands.command(name="play", pass_context=True)
    async def _play_song(self, ctx, *, uri: str = None):
        if uri is not None:
            song = self.play_song(uri)
        else:
            self.sp.start_playback()
            sleep(0.1)
            song = self.sp.current_user_playing_track()

        if song is not None:
            await ctx.send(embed=self.create_song_embed(song, "Now Playing"))
        else:
            await ctx.send(embed=Embed(title="No Song playing", color=Color.red()))

    # TODO make host/admin only
    @commands.command(name="pause", pass_context=True)
    async def _pause_playback(self, ctx):
        self.sp.pause_playback()
        # self.stop_autoplay() TODO AUTOPLAY
        await ctx.send(embed=Embed(title="Pausing playback"))

    @commands.command(name="next", pass_context=True)
    async def _song_up_next(self, ctx):
        song = self.play_next_song()

        if song is not None:
            await ctx.send(embed=self.create_song_embed(song, "Now Playing"))
        else:
            await ctx.send(embed=Embed(title="No song in queue", color=Color.red()))

    @commands.command(name="prev", pass_context=True)
    async def _previous_track(self, ctx):
        self.sp.previous_track()
        sleep(0.1)
        song = self.sp.current_user_playing_track()
        if song is not None:
            await ctx.send(embed=self.create_song_embed(song, "Now Playing"))
        else:
            await ctx.send(embed=Embed(title="No Song playing", color=Color.red()))

    @commands.command(name="queue", pass_context=True)
    async def _queue_song(self, ctx, *, uri: str = None):
        if uri is not None:
            track = self.sp.track(uri)
            if track is not None:
                self.discord_queue.append(track['uri'])
                await ctx.send(embed=self.create_track_embed(track, "Song queued"))
            else:
                await ctx.send(embed=Embed(title="Invalid song uri or url",
                                           description="My search came up empty, please check your uri/url",
                                           color=Color.red()))
        else:
            await ctx.send(embed=Embed(title="Missing song url",
                                       description="Correct usage of the command:\nqueue [spotify url or uri]",
                                       color=Color.red()))

    # TODO make sub commands for playlist or album

    # TODO Make owner only
    @commands.command(name="out", pass_context=True)
    async def _set_standard_channel(self, ctx):
        self.set_stdout(ctx.message.channel.id)
        await ctx.send(embed=Embed(title="New out channel set for spotify",
                                   description=f"New channel: <#{ctx.message.channel.id}>",
                                   color=Color.blue()))
