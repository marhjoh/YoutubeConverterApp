import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from downloader import download_video

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

        self.progress['value'] = 0
        download_video(url, format, quality, self.output_path, self.update_progress)

    def choose_directory(self):
        self.output_path = filedialog.askdirectory()
        if self.output_path:
            self.output_label.config(text=self.output_path, fg="green")
        else:
            self.output_label.config(text="No directory chosen", fg="red")