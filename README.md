# YouTube Chan
A discord bot to play YouTube audio on voice channels. This bot has the intent of replacing **only** the youtube player functionality
that was offered by bots like **Rythm** and **Groovy** that recently stopped their service. At the moment the bot is very simple and only 
supports operations like play, skip, add to queue, pause, resume, stop, etc. In the near future I may add spotify functionality but I'm not making any promises.
Below I give some instructions on how you can use this bot for personal uses with one of the free tier vm's offered by Google Cloud, AWS, Azure, Digital Ocean, etc... This bot is running
on a personal server and I'm hosting it on Google cloud with a `e2-micro` instance running Ubuntu 20.04 (LTS).

# Bot Commands
The default prefix is `?` however you can set this when you start the bot.

1. `?play [URL]`: Plays the video or adds it to queue if there is a video currently playing. The URL can be a single video or a playlist 
2. `?queue`: Sends a message to the channel with all the videos in the queue.
3. `?skip`: Skips the current video. 
4. `?pause`: Pauses the player 
5. `?resume`: Resumes the player
6. `?stop`: Stops the player and clears the queue.
7. `?join`: Joins the current voice channel (you need to be in one).
8. `?shuffle`: Shuffles the queue.
9. `?remove [SONG NUMBER]`: Removes the video at index `SONG NUMBER`
10. `?commands`: Sends message with all the commands.

# Requirements
This bot runs primarily with three libraries `discord.py`, `youtube-dl` and `ffmpeg`. To install them on a -nix like box you can run the following commands:

```bash
# Install dependencies for discord[voice] and ffmpeg
sudo apt install -y libffi-dev libnacl-dev python3-dev ffmpeg

# Install discord.py with voice support
python3 -m pip install -U discord.py[voice]

# Install youtube-dl
pip install --upgrade youtube-dl
```

# Hosting and running the bot
Before you start you need to make sure you have a token (with persmissions to write and join voice channels), 
there are many tutorials on how to setup a discord app so I will assume you have one already.
Pick a cloud provider and launch a VM instance with your desired specs and os, in my case I will be hosting the bot on a `e2-micro` (2 vCPU, 1GB memory) instance running Ubuntu 20.04
on GCP, this is enough for using on one server. Once you have the instance up a running there are a couple of steps you need to take, first setup a non-root user,
enable the firewall, download dependencies and source code and finally start the server. SSH into your VM and follow this steps:

```bash
# Running Ubuntu 20.04 (LTS)
# Setup non-root user with sudo permissions
adduser sam
usermod -aG sudo sam

# Set up firewall only allow ssh
sudo ufw allow 22/tcp
sudo ufw enable

# Update and upgrade packages
sudo apt update && sudo apt upgrade -y

# Reboot the machine wait a few minutes and ssh back in
sudo reboot
```
When you ssh back in with the new user you can download the source code, setup a python virtual environment and run the bot. 

```bash
# Make sure you have pip installed
sudo apt-get install python3-pip

# If you have pip upgrade it to the latest version
python3 -m pip install --upgrade pip

# Install venv
sudo apt install -y pyton3-venv libffi-dev libnacl-dev python3-dev ffmpeg

# On a directory of your choosing clone the repo and set up a virtual env
git clone https://github.com/cesar-yoab/youtube-chan && cd youtube-chan/
python3 -m venv .venv
source ./.venv/bin/activate
python3 -m pip install --upgrade pip

# Install python requirements
# Install discord.py with voice support
python3 -m pip install -U discord.py[voice]

# Install youtube-dl
pip install --upgrade youtube-dl

# Run the bot
python ytchan --token YOUR_TOKEN_HERE
```

# Resources
Here are some resources used in the creation of this bot:

- [discord.py docs](https://discordpy.readthedocs.io/en/stable/index.html#)
- [Formating text](https://python.plainenglish.io/python-discord-bots-formatting-text-efca0c5dc64a)
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)
