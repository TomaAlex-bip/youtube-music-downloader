import os
import subprocess
import traceback
from multiprocessing import Value
import queue
import threading
from pytube import Playlist
from mutagen.easyid3 import EasyID3
import song_name_filter


class PlaylistDownloader:
    def __init__(self):
        self.directory_to_download = ""
        self.playlist_link = ""
        self.songs_queue = queue.Queue()
        self.downloaded_files = Value('i', 0)
        self.download_threads = []
        self.download_threads_count = 20

    def read_user_input(self):
        self.playlist_link = input("Enter Youtube playlist link: ")
        while len(self.playlist_link) < 5:
            self.playlist_link = input("Invalid link, try again: ")

        self.directory_to_download = input("Enter folder name to store your downloads: ")

    def download_song(self, thread_index=-1):
        while True:
            video = None
            try:
                video = self.songs_queue.get(timeout=5, block=True)
                download_path = f'../Playlists/{self.directory_to_download}'
                out_file = video.streams.filter(only_audio=True, abr="160kbps").first().download(output_path=download_path)
                song_title, artist_name = song_name_filter.filter_song(video.title, video.author)
                subprocess.run(f'ffmpeg -i "{out_file}" "{download_path}/{song_title}".mp3', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                os.remove(out_file)
                new_file = EasyID3(f"{download_path}/{song_title}.mp3")
                new_file['artist'] = artist_name
                new_file.save()
                self.downloaded_files.value += 1
                print(f"\tDownloaded {self.downloaded_files.value}: {song_title} --- Artist: {artist_name}")

            except queue.Empty:
                print(f"Thread {thread_index} finished work (empty queue)!")
                break

            except Exception as ex:
                print(f"Error: Thread {thread_index} encountered unexpected error: {ex} retying download!")
                # traceback.print_exception(ex)
                if video is not None:
                    self.songs_queue.put(video)

    def download_playlist(self):
        self.playlist = Playlist(self.playlist_link)
        if len(self.directory_to_download) < 1:
            self.directory_to_download = self.playlist.title

        print(f'Started download of playlist: {self.playlist.title}')

        for i in range(self.download_threads_count):
            t = threading.Thread(target=self.download_song, args=[i])
            t.start()
            self.download_threads.append(t)

        for video in self.playlist.videos:
            self.songs_queue.put(video)

        for i in range(self.download_threads_count):
            self.download_threads[i].join()

        print(f'\n --- Download completed with {self.downloaded_files.value} files')


def main():
    try:
        pd = PlaylistDownloader()
        pd.read_user_input()
        pd.download_playlist()
    except KeyboardInterrupt:
        quit(0)


if __name__ == '__main__':
    main()
