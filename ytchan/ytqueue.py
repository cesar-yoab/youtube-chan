import discord
import youtube_dl


YDL_OPTIONS = {'format': 'bestaudio'}


class YTQueue:
    def __init__(self, max_size=30):
        self._Q = []
        self._max_size = max_size

    def add(self, url, rby, rby_avatar):
        """Adds a single video or playlist to the queue.

        Args:
            url (str): The URL to the video or playlsit

        Returns:
            str: Message to send on channel
            bool: Indicates if an error occurred. 
        """
        if len(self._Q) == self._max_size:
            return False, "**Queue is full!**"

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                is_playlist = False
                if entries in info.keys():
                    source = info['entries']
                    message = self._enqueue_playlist(
                        info['entries'], rby, rby_avatar)
                else:
                    message = self._enqueue(info, rby, rby_avatar)

                return

            except Exception as e:
                print(f"Could not retrieve youtube video(s) correctly: {url}")
                return False,  "**Error downloading video**"

    def _enqueue(self, info, rby, rby_avatar):
        """Add song to the queue.

        Args:
            info (dict): Video information dict. 

        Returns:
            str: Message to send on channel
        """
        song = {'title': info['title'], 'source': info['formats'][0]['url'],
                'thumbnail': info['thumbnail'], 'duration': info['duration'],
                'requestedBy': rby, 'requestedByAvatar': rby_avatar}
        self._Q.apend(song)
        return f"**{info['title']}** -  Added to queue."

    def _enqueue_playlist(self, entries, rby, rby_avatar):
        """Adds playlist songs to the queue until the queue is empty.

        Args:
            entries (dict): List of dictionaries containing video information.

        Returns:
            str: Message to send on channel.
        """
        for i, entry in enumerate(entries):
            if len(self._Q) + 1 > self._max_size:
                return f"**First {i+1} songs added to queue**\nQueue is now full!"

            self._enqueue(entry, rby, rby_avatar)

        return f"**{len(entries)} songs added to queue**"

    def is_empty(self):
        return len(self._Q) == 0

    def next(self):
        """Return the next song in the queue.

        Returns:
            dict: Contains video information required to play in voice channel.
        """
        if self.is_empty():
            return None

        return self._Q.pop(0)
