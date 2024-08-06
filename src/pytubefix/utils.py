from moviepy.editor import VideoFileClip
from proglog import ProgressBarLogger
from pytubefix import YouTube
from datetime import datetime
import unicodedata
import threading
import traceback
import logging
import shutil
import os

class YouTubeDownloader:
    def __init__(self, url: str):
        self.url = url
        self.yt = YouTube(url, on_progress_callback=self.progress_callback)
        self.progress = 0
    
    @property
    def streams(self):
        available_streams = {"Video": [], "Audio": []}
        try:
            videos = self.yt.streams.filter(type="video", progressive=True)
            if len(videos):
                stream = videos.order_by("resolution").desc().first()
                available_streams["Video"] = [stream.url, stream.resolution, self._format_size(stream.filesize), stream.subtype.upper()]

            audios = self.yt.streams.filter(type="audio")
            if len(audios):
                stream = audios.order_by("abr").desc().first()
                available_streams["Audio"] = [stream.url, stream.abr, self._format_size(stream.filesize), "MP3"]

        except:
            logging.exception(f"Failed to get stream from {self.url}")

        return available_streams
    
    @property
    def thumbnail_url(self):
        return self.yt.thumbnail_url
    
    @property
    def title(self):
        return self.yt.title

    @property
    def length(self):
        return self.yt.length

    def _format_size(self, filesize):
        units, unit = ["kb", "mb", "gb"], "b"
        for u in units:
            if filesize > 1000:
                filesize /= 1000
                unit = u
            else:
                return f"{int(filesize)} {unit.upper()}"

    def progress_callback(self, stream, chunk, bytes_remaining):
        filesize = stream.filesize
        bytes_received = filesize - bytes_remaining
        self.progress = bytes_received / filesize

        # self.download_type = download_type
        # self.output_dir = output_dir
        # self._progress = [0.0]
        # self.filename = None
        # self.srcname = None
        # self.is_downloaded = False
        # self.error_message = ""
        # self.convert_logger = None if download_type == "video" else Video2AudioLogger(progress=self._progress)
        # self.start()

    # def download(self, stream, mp3=False):
    #     logging.info(f"Start to download {stream} ...")
    #     return stream.download(
    #         self.output_dir,
    #         filename=datetime.now().strftime("%Y%m%d_%H%M%S_%f") + f".{stream.subtype}",
    #         mp3=mp3
    #     )

    # def run(self):
    #     try:
    #         if os.path.isdir(self.output_dir):
    #             shutil.rmtree(self.output_dir)

    #         yt = YouTube(self.url, on_progress_callback=self.progress_callback)

    #         streams_for_audio = yt.streams.filter(type="audio")
    #         streams_for_video = yt.streams.filter(type="video")

    #         if self.download_type == "video":
    #             is_valid = len(streams_for_audio) > 0 and len(streams_for_video) > 0
    #         else:
    #             is_valid = len(streams_for_audio) > 0
            
    #         if not is_valid:
    #             self.error_message = f"This URL does not support {self.download_type} downloading"

    #         elif self.download_type == "video":
    #             video = streams_for_video.order_by("resolution").desc().first()
    #             video_path = self.download(video)
    #             audio = streams_for_audio.order_by("abr").desc().first()
    #             audio_path = self.download(audio, mp3=True)
    #             print(video_path, audio_path)

            # else:


            # video > streams_for_video + streams_for_audio
            # audio > streams_for_audio

            # if len(streams_for_audio):
            #     stream_for_video = streams.order_by("resolution").desc().first()
            #     stream_for_audio = streams.order_by("resolution", progressive=True).asc().first()
            #     filename = stream.download(
            #         self.output_dir, filename=datetime.now().strftime("%Y%m%d_%H%M%S_%f") + f".{stream.subtype}")
            #     if self.download_type == "video":
            #         self.srcname = f"{stream.title}.{stream.subtype}"
            #         self.filename = filename
            #     else:
            #         dst = os.path.splitext(filename)[0] + ".mp3"
            #         video_clip = VideoFileClip(filename)
            #         audio_clip = video_clip.audio
            #         audio_clip.write_audiofile(dst, logger=self.convert_logger)
            #         audio_clip.close()
            #         video_clip.close()
            #         self.srcname = f"{stream.title}.mp3"
            #         self.filename = dst

            # else:
            #     self.error_message = f"This URL does not support {self.download_type} downloading"
                
#         except:
#             self.error_message = traceback.format_exc()
        
#         if self.error_message == "":
#             logging.info(f"Successfully download {self.filename} from {self.url}")
#         else:
#             logging.warning(f"Failed to download from {self.url}: {self.error_message}")

#         self._progress[0] = 1
    
#     @property
#     def progress(self):
#         return self._progress[0]

#     def progress_callback(self, stream, chunk, bytes_remaining):
#         filesize = stream.filesize
#         bytes_received = filesize - bytes_remaining

#         if self.convert_logger is None:
#             self._progress[0] = bytes_received / filesize
#         else:
#             self._progress[0] = bytes_received / filesize / 2

# class Video2AudioLogger(ProgressBarLogger):
#     def __init__(self, *args, **kwargs):
#         self._progress = kwargs.pop("progress")
#         super().__init__(*args, kwargs)

#     def bars_callback(self, bar, attr, value, old_value=None):
#         percentage = value / self.bars[bar]["total"]
#         self._progress[0] = 0.5 + percentage / 2