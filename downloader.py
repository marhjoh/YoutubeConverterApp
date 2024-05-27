import os
import re
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError, PytubeError
from moviepy.video.io.VideoFileClip import VideoFileClip

def validate_url(url):
    """
    Validate the given YouTube URL.
    """
    youtube_regex = re.compile(
        r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
    )
    return re.match(youtube_regex, url) is not None

def download_video(url, format, quality, output_path, progress_callback):
    if not validate_url(url):
        raise ValueError("Invalid YouTube URL")

    try:
        yt = YouTube(url, on_progress_callback=progress_callback)
        stream = yt.streams.filter(progressive=True, file_extension="mp4").first() if format == "MP4" else yt.streams.filter(only_audio=True).first()

        if stream is None:
            raise VideoUnavailable(f"No stream available for the format: {format}")

        output_file = stream.download(output_path=output_path)

        if format == "MP3":
            base, ext = os.path.splitext(output_file)
            new_file = base + ".mp3"
            try:
                VideoFileClip(output_file).audio.write_audiofile(new_file)
                os.remove(output_file)
            except Exception as e:
                os.remove(output_file)
                raise e

    except RegexMatchError:
        raise ValueError("Invalid YouTube URL format.")
    except VideoUnavailable:
        raise ValueError("The video is unavailable. Please check the URL or try another video.")
    except PytubeError:
        raise ValueError("An error occurred with Pytube. Please try again.")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")