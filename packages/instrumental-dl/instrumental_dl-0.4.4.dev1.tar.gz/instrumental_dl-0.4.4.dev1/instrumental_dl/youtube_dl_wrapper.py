import youtube_dl

from .common.io import rename_all_files
from .url_query import get_urls
from .common.path import goto_music


class YoutubeDL:
    """A class used as a wrapper for youtube-dl.

    Attributes:
        options -- The options used to download and convert
                   using youtube-dl.
        logger --  The main logger object.
    """

    def __init__(self, logger):
        self.logger = logger
        self.options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': self.logger,
            'progress_hooks': [self.logger.hook],
            'nocheckcertificate': True,
            'outtmpl': '%(title)s.%(ext)s',
        }

    def download_songs(self, song_names: list):
        """Downloads all of the instrumentals in song_names using youtube-dl.

        :param: song_names: A list of all the song names to be downloaded."""
        # Moves current directory to music/Instrumentals/
        goto_music()
        # Get urls to download and lists to log
        urls, failed_songs, song_names = get_urls(self.logger, song_names)
        if len(failed_songs) > 0:
            self.logger.add_failed_songs(failed_songs)
        self.logger.add_song_titles(song_names)
        # Downloads all instrumentals
        with youtube_dl.YoutubeDL(self.options) as ydl:
            ydl.download(urls)

        rename_all_files(self.logger)
