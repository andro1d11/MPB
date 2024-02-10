import lyricsgenius


class lyrics_parser():
    def __init__(self, debug):
        self.genius = lyricsgenius.Genius('h-J2AE3-yID_bYSQ9inTQrBr4NHP1YswUpOoVuAkLLOJOOQjjaTNYo71RrOiqbDNo5mitRAs8KOoq5DOv47ONg')
        self.connection = True

    def get_tracks(self, track_name):
        data = {}
        req = self.genius.search(track_name)
        for i in req['hits']:
            if i['result']['_type'] == 'song':
                title = i['result']['full_title']
                url = i['result']['relationships_index_url']
                if url.split('-')[-1] == 'sample':
                    url = url[:-6]
                    url += 'lyrics'
                data[title] = url
        return data

    def get_lyrics(self, url):
        return self.genius.lyrics(song_url=url)

if __name__ == '__main__':
    t1 = lyrics_parser(True)
    a = t1.get_tracks('BOOKER - Жилы')
    print(a)