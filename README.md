# SpotCord - Spotify listening party in Discord

![][tag-lisence]
![][tag-issues]
![][tag-pull]

> A minimal Discord Bot for controlling an spotify instance. The host connects his spotify account to the bot. Others can then listen along and use the bot to queue up songs. 

## Discord Hackweek
This bot was made during Discord's hackweek as my submission. It was created for as often when listening along with people on spotify you might want to share a song or just collaboratively with your friends choose what to listen too.

SpotCord allows people to queue up songs on the host's spotify, removing the hazel from the host, which can just lay back and enjoy the music. 

## Installation
There are two ways of running SpotCord, you can run it locally or with docker.
The first step though is to create your bot account and a Spotify developer account.

The process of creating a Discord bot is described a lot of places, so i will just leave you with [this](https://discordpy.readthedocs.io/en/latest/discord.html). Remember your token, you are gonna need it later.

Next thing you are gonna need an Spotify app, and spotify them self have been so kind to describe how to do that [here](https://developer.spotify.com/documentation/general/guides/app-settings/).
They are gonna ask you for a website and a redirect URI, just what ever for the website or nothing at all, and for the URI use `http://localhost/`. Later we are gonna use the Client ID and Secret, so write that down.


### Local Installation
To run the bot it requires you to have Python 3.6+ installed.
Clone the code using git:
```text
git clone https://github.com/LukasRH/SpotCord.git
```
Then `cd` into the directory using the terminal and install the requirements
````text
pip install -r requirements.txt
````
Now you must download the submodules too, which is done with the following two commands:
```text
git submodule init
git submodule update
```

### Docker
The docker image for SpotCord is hosted on DockerHub, and therefor it can be deployed with only a few commands and there are no need to download or clone the code.
```text
docker pull lukerh/spotcord
```
If you want to build the image yourself you are free to do so too, by downloading or cloning the code and running the following commands.
Download or clone the code using git:
```text
git clone https://github.com/LukasRH/SpotCord.git
```
Then `cd` into the directory using the terminal and start the build:
```text
docker build --rm -t spotcord
```

## Starting the bot
Starting the bot requires setting the bot token, spotify id and secret as environment variables, depending on how you installed the bot this is done differently.
### Local bot
On windows setting environment variables can be done by using the `set` command, you will have to set these variables again if you close the process.
```text
set BOT_TOKEN="your token here"
set BOT_PREFIX="The prefix you want the bot to react on"
set USER_ID="Your spotify username"
set CLIENT_ID="Your spotify ID"
set CLIENT_SECRET="Your spotify Secret"
set CHANNEL_ID="The id of the default channel, to post autoplay messages in"
```
On linux this can be done by the following:
```text
export BOT_TOKEN="your token here"
export BOT_PREFIX="The prefix you want the bot to react on"
export USER_ID="Your spotify username"
export CLIENT_ID="Your spotify ID"
export CLIENT_SECRET="Your spotify Secret"
export CHANNEL_ID="The id of the default channel, to post autoplay messages in"
```

SpotCord can now by started my running it in python.
````text
python main.py
````
### Using Docker
The bot can be started with the `docker run` command and by specifying the environment variables.
```text
docker run --restart=on-failure --rm -e "BOT_TOKEN=YourToken" -e "BOT_PREFIX=BotPrefix" -e "USER_ID=SpotifyUserName" -e "CLIENT_ID=SpotifyID" -e "CLIENT_SECRET=SpotifySecret" -e "CHANNEL_ID=DiscordChannelID" spotcord
```

### Logging in to Spotify using the bot
The first time Spotcord starts it will ask you to sign into Sporify. It will open your default web browser, and if not it will show the link you have to go to.
Log in on the provided link, after you have logged in you will be redirected to an empty page, copy the URL of this page and paste it into the bot's terminal and press enter.
If done correctly you should see the a confirmation message, and the bot is now up and running. This should only be necessary the first time, and if the credentials expire.

## Dependencies
[Python 3.6+](https://www.python.org/)

[Discord.py](https://github.com/Rapptz/discord.py)

requests

six

## Reporting Issues
If you have suggestions, bugs or other issues specific to this library, file them [here](https://github.com/LukasRH/SpotCord/issues). Or just send me a pull request.

## Find me on Discord ![][tag-discord]
> LukeRH#0001

[![InviteBanner](https://user-images.githubusercontent.com/16747705/60059041-111b6600-96eb-11e9-9c26-6c0e8e9b9164.png)](https://discord.gg/PyKMjq8)

<!-- Markdown link & img dfn's -->
[tag-lisence]: https://img.shields.io/github/license/LukasRH/SpotCord.svg?style=flat-square
[tag-issues]: https://img.shields.io/github/issues/LukasRH/SpotCord.svg?style=flat-square
[tag-pull]: https://img.shields.io/github/issues-pr/LukasRH/spotcord.svg?style=flat-square
[tag-discord]: https://img.shields.io/discord/580822439773208581.svg


