# YouTube Chan
A discord bot to play YouTube audio on voice channels. This bot has the intent of replacing **only** the youtube player functionality
that was offered by bots like **Rythm** and **Groovy** that recently stopped their service. At the moment the bot is very simple and only 
supports operations like play, skip, add to queue, pause, resume, stop, etc. In the near future I may add spotify functionality but I'm not making any promises.
Below I give some instructions on how you can use this bot for personal uses with one of the free tier vm's offered by Google Cloud, AWS or Azure.

# Bot Commands
The default prefix is `?` however you can set this when you start the bot.

1. `?play [URL]`: Plays the video or adds it to queue if there is a video currently playing. The URL can be a single video or a playlist 
2. `?queue`: Sends a message to the channel with all the videos in the queue.
3. `?skip`: Skips the current video. 
4. `?skipto [SONG NUMBER]`: Skips to the video at index `SONG NUMBER`
5. `?pause`: Pauses the player 
6. `?resume`: Resumes the player
7. `?stop`: Stops the player and clears the queue.
8. `?join`: Joins the current voice channel (you need to be in one).
9. `?shuffle`: Shuffles the queue.
10. `?remove [SONG NUMBER]`: Removes the video at index `SONG NUMBER`


## Requirements
This bot runs primarily with three libraries `discord.py`, `youtube-dl` and `ffmpeg`. To install them on a -nix like box you can run the following commands:

```bash
# Install dependencies for to use voice
sudo apt install -y libffi-dev libnacl-dev python3-dev ffmpeg

# Install discord.py with voice support
python3 -m pip install -U discord.py[voice]

# Install youtube-dl (need sudo permissions)
pip install --upgrade youtube-dl
```

# Resources
Here are some resources used in the creation of this bot:

- [discord.py docs](https://discordpy.readthedocs.io/en/stable/index.html#)
- [Formating text](https://python.plainenglish.io/python-discord-bots-formatting-text-efca0c5dc64a)

https://github.com/Gaming-Rowdies/cs-music/blob/d743ce7aff0eecb2e23e230fa44d4a279db85be5/bot.py