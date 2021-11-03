# youtube-chan
A discord music bot

## Requirements
This bot runs primarily with three libraries `discord.py`, `youtube-dl` and `ffmpeg`. To install them on a -nix like box you can run the following commands:

```bash
# Install dependencies for to use voice
apt install libffi-dev libnacl-dev python3-dev

# Install discord.py with voice support
python3 -m pip install -U discord.py[voice]

# Install youtube-dl (need sudo permissions)
sudo -H pip install --upgrade youtube-dl

# Finally you will also need ffmpeg to stream audio
sudo apt install -y ffmpeg
```