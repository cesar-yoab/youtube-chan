<p align="center">
   <img src="https://raw.githubusercontent.com/cesar-yoab/youtube-chan/main/.github/youtube-chan-github.png" width="200">
</p>

[![image](https://img.shields.io/github/license/cesar-yoab/youtube-chan)](https://github.com/cesar-yoab/youtube-chan/blob/main/LICENSE)
![image](https://img.shields.io/badge/docker--build-passing-green)

# YouTube Chan
This is a simple Discord bot that allows you to play audio from YouTube videos in a voice channel. The bot uses the 
[discord.py](https://github.com/Rapptz/discord.py) library to interface with Discord and the [youtube-dl](https://github.com/ytdl-org/youtube-dl/) 
library to extract audio from YouTube videos.

## Usage

To use the bot, invite it to your Discord server and use the following commands in a text channel:

- `?play <youtube_url>`: Plays the audio from the Youtube video or playlist provided.
- `?skip`: Skips the current song and plays the next one in the queue.
- `?pause`: Pause the current playing audio
- `?stop`: Stops the current song and leaves the voice channel.

Alternatively you can use the controls in the discord channel directly.

## Installation

To install the bot on your own server I have provided a Docker file that will run the code inside a container.
If you however wish to run directly from source then:

1. Clone or download the repository to your local machine.
2. Install the dependencies by running pip install -r requirements.txt in the project directory.
3. Create a new application and bot account in the [Discord Developer Portal](https://discord.com/developers/applications).
4. Copy the bot token and create a file named .env in the project directory with the following contents: `DISCORD_TOKEN=<your_bot_token>`
5. Run the bot using the command python bot.py in the project directory.

## Configuration
You can customize the bot's behavior by editing the config.json file in the project directory. The available options are:

- `prefix`: The prefix used to invoke bot commands. Default is !.
- `maxQueueSize`: The maximum number of songs that can be in the queue. Default is 10.

## License
This project is licensed under the [MIT License](https://github.com/cesar-yoab/youtube-chan/blob/main/LICENSE). 
Feel free to use, modify, and distribute it however you like. 
If you find any bugs or have any suggestions for improvement, please open an issue or a pull request on the GitHub repository. 
IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.