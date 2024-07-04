import os
from pytube import YouTube
from tkinter import filedialog



class YoutubeDownloader:

    selected_output = ''

    percentage_of_completion = '0'

    stop_progress = False

    def create_yt_object(self, with_url):
        try:
            yt = YouTube(with_url, on_progress_callback=self.on_progress)
            return yt
        except Exception as e:
            print(f'Error {e}')


    def download_video(self, with_url):
        d_video = self.create_yt_object(with_url).streams.filter(file_extension='mp4').order_by('resolution').last()
        d_video.download(output_path=self.selected_output)


    def select_folder(self):
        self.selected_output = filedialog.askdirectory()
        print(self.selected_output)

    
    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        self.percentage_of_completion = str(int(bytes_downloaded / total_size * 100))


youtube_downloader_object = YoutubeDownloader()