from youtubesearchpython import VideosSearch, Playlist
from urllib.error import HTTPError
import requests
import yt_dlp
import pafy
import os


class youtube_parser():
    def __init__(self, debug):
        self.ban_cymbols = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
        self.connection = True

    def get_urls(self, track_name):
        videosSearch = VideosSearch(track_name, limit = 20)
        result = videosSearch.result()['result']
        data = {}
        for i in result:
            url = f"https://www.youtube.com/watch?v={i['id']}"
            title = i['title']
            img_url = i['thumbnails'][0]['url']
            data[self.delete_ban_cymbols(title)] = (url, img_url)
        return data

    def get_playlist(self, playlist_url):
        result = Playlist(playlist_url)
        while result.hasMoreVideos:
            result.getNextVideos()
        data = {}
        for i in result.videos:
            url = f"https://www.youtube.com/watch?v={i['id']}"
            title = i['title']
            img_url = i['thumbnails'][0]['url']
            data[self.delete_ban_cymbols(title)] = (url, img_url)
        return data

    def get_title(self, url):
        result = pafy.new(url)
        return self.delete_ban_cymbols(result.title)

    def get_best_audio(self, url):
        result = pafy.new(url)
        return result.getbestaudio().url

    def get_clear_url(self, url):
        if url.split('/watch?v=')[0] == 'https://www.youtube.com':
            return url[0:43]
        
    def delete_ban_cymbols(self, text):
        for c in self.ban_cymbols:
            text = text.replace(c, '')
        return text

    def rename_files(self, path):
        for i in os.listdir(path):
            file_name = i
            extension = i.split('.')[1]
            if extension in ['3gp', 'm4a', 'm4v', 'mp4', 'webm', 'ogg']:
                clear_file_name = file_name[:-len(list(extension)) - 1]
                while True:
                    try:
                        os.rename(f'{path}/' + i, f'{path}/' +
                                  str(clear_file_name) + '.mp3')
                        break
                    except PermissionError:
                        pass


    def download_track(self, url, img, path, track_name):
        print(f'DOWNLOAD_TRACK STARTED:\t{track_name}')
        for i in range(3):
            try:
                url = self.get_clear_url(url)
                result = pafy.new(url)
                if img == None:
                    img = result.getbestthumb()
                    track_name = result.title
                    for c in self.ban_cymbols:
                        track_name = track_name.replace(c, '')
                try:
                    image = requests.get(img)
                    with open(f'extra/files/{track_name}.jpg', 'wb') as f:
                        f.write(image.content)
                except:
                    pass

                ydl_opts = {
                    'outtmpl': f'{path}/{track_name}.mp3',
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                break
            except HTTPError:
                print('Trying again')
            except yt_dlp.utils.DownloadError:
                break
        return track_name

if __name__ == "__main__":
    t1 = youtube_parser(True)
    #t1.get_playlist()
    #t1.download_track('https://www.youtube.com/watch?v=ezVna4umnyk', '', '', 'svechi')
    #print(t1.get_urls('Погасли свечи'))