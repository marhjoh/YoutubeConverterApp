import os
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError, PytubeError
from moviepy.video.io.VideoFileClip import VideoFileClip
from utils import validate_url, setup_logging
import logging

setup_logging()

def download_video(url, format, quality, output_path, progress_callback):
    """
    Download and convert a YouTube video to the specified format.

    Args:
        url (str): The URL of the YouTube video.
        format (str): The desired output format ("MP3" or "MP4").
        quality (str): The desired quality for MP4 format ("720p" or "1080p").
        output_path (str): The directory where the output file will be saved.
        progress_callback (function): Callback function to update download progress.
    """
    logger = logging.getLogger(__name__)

    if not validate_url(url):
        logger.error("Invalid YouTube URL: %s", url)
        raise ValueError("Invalid YouTube URL")

    try:
        yt = YouTube(url, on_progress_callback=progress_callback)
        stream = yt.streams.filter(progressive=True, file_extension="mp4").first() if format == "MP4" else yt.streams.filter(only_audio=True).first()

        if stream is None:
            logger.error("No stream available for the format: %s", format)
            raise VideoUnavailable(f"No stream available for the format: {format}")

        output_file = stream.download(output_path=output_path)
        logger.info("Downloaded video: %s", output_file)

        if format == "MP3":
            base, ext = os.path.splitext(output_file)
            new_file = base + ".mp3"
            try:
                VideoFileClip(output_file).audio.write_audiofile(new_file)
                os.remove(output_file)
                logger.info("Converted to MP3: %s", new_file)
            except Exception as e:
                os.remove(output_file)
                logger.error("Error during conversion to MP3: %s", str(e))
                raise e

    except RegexMatchError:
        logger.error("Invalid YouTube URL format: %s", url)
        raise ValueError("Invalid YouTube URL format.")
    except VideoUnavailable:
        logger.error("Video unavailable: %s", url)
        raise ValueError("The video is unavailable. Please check the URL or try another video.")
    except PytubeError as e:
        logger.error("Pytube error: %s", str(e))
        raise ValueError("An error occurred with Pytube. Please try again.")
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")