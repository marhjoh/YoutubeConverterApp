import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError, PytubeError


class YouTubeConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video to MP3/MP4 Converter")
        self.create_widgets()

    def create_widgets(self):
        self.url_label = tk.Label(self.root, text="YouTube URL:")
        self.url_label.pack(pady=5)
        self.url_entry = tk.Entry(self.root, width=50)
        self.url_entry.pack(pady=5)

        self.format_label = tk.Label(self.root, text="Select Format:")
        self.format_label.pack(pady=5)
        self.format_var = tk.StringVar(value="MP4")
        self.format_option = tk.OptionMenu(self.root, self.format_var, "MP3", "MP4")
        self.format_option.pack(pady=5)

        self.quality_label = tk.Label(self.root, text="Select Quality (MP4 only):")
        self.quality_label.pack(pady=5)
        self.quality_var = tk.StringVar(value="720p")
        self.quality_option = tk.OptionMenu(self.root, self.quality_var, "720p", "1080p")
        self.quality_option.pack(pady=5)

        self.output_button = tk.Button(self.root, text="Choose Output Directory", command=self.choose_directory)
        self.output_button.pack(pady=5)
        self.output_label = tk.Label(self.root, text="No directory chosen", fg="red")
        self.output_label.pack(pady=5)

        self.download_button = tk.Button(self.root, text="Download", command=self.download_video)
        self.download_button.pack(pady=20)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=20)

    def update_progress(self, stream, chunk, bytes_remaining):
        size = self.stream.filesize
        progress = (size - bytes_remaining) / size * 100
        self.progress['value'] = progress
        self.root.update_idletasks()

    def download_video(self):
        url = self.url_entry.get()
        format = self.format_var.get()
        quality = self.quality_var.get()

        if not url or not hasattr(self, 'output_path'):
            messagebox.showerror("Error", "Please provide a valid URL and choose an output directory.")
            return

        if not self.validate_url(url):
            messagebox.showerror("Error", "Please provide a valid YouTube URL.")
            return

        try:
            yt = YouTube(url, on_progress_callback=self.update_progress)
            self.stream = yt.streams.filter(progressive=True,
                                            file_extension="mp4").first() if format == "MP4" else yt.streams.filter(
                only_audio=True).first()

            if self.stream is None:
                raise VideoUnavailable(f"No stream available for the format: {format}")

            self.progress['value'] = 0
            output_file = self.stream.download(output_path=self.output_path)

            if format == "MP3":
                base, ext = os.path.splitext(output_file)
                new_file = base + ".mp3"
                try:
                    VideoFileClip(output_file).audio.write_audiofile(new_file)
                    os.remove(output_file)
                except Exception as e:
                    os.remove(output_file)
                    raise e

            messagebox.showinfo("Success", "Download and conversion completed successfully!")
        except RegexMatchError:
            messagebox.showerror("Error", "Invalid YouTube URL format.")
        except VideoUnavailable:
            messagebox.showerror("Error", "The video is unavailable. Please check the URL or try another video.")
        except PytubeError:
            messagebox.showerror("Error", "An error occurred with Pytube. Please try again.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def validate_url(self, url):
        """
        Validate the given YouTube URL.
        """
        youtube_regex = re.compile(
            r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
        )
        return re.match(youtube_regex, url) is not None

    def choose_directory(self):
        self.output_path = filedialog.askdirectory()
        if self.output_path:
            self.output_label.config(text=self.output_path, fg="green")
        else:
            self.output_label.config(text="No directory chosen", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeConverterApp(root)
    root.mainloop()