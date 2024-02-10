from prs_youtube import youtube_parser
from prs_lyrics import lyrics_parser
from prs_lastfm import lastfm_parser
import threading


class init_parsers():
    def __init__(self, debug=False):
        self.parsers_done = 0
        self.result = None
        self.debug = debug

    def init_parser_lyrics(self):
        self.parser_lyrics = lyrics_parser(self.debug)
        self.parsers_done += 1

    def init_parser_youtube(self):
        self.parser_youtube = youtube_parser(self.debug)
        self.parsers_done += 1

    def init_parser_lastfm(self):
        print(1)
        self.parser_lastfm = lastfm_parser(self.debug)
        self.parsers_done += 1

    def start_threads(self):
        t1 = threading.Thread(target=self.init_parser_lyrics)
        t2 = threading.Thread(target=self.init_parser_youtube)
        t3 = threading.Thread(target=self.init_parser_lastfm)
        parsers = [t1, t2, t3]
        parsers_done = 0
        for i in parsers:
            i.start()
        while parsers_done != 3:
            for i in parsers:
                if i.is_alive() == False:
                    parsers.remove(i)
                    parsers_done += 1
        self.result = self.parser_lyrics, self.parser_youtube, self.parser_lastfm
