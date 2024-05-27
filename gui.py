import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from downloader import download_video
from utils import setup_logging
from PIL import Image, ImageTk  # Make sure to install Pillow

# Initialize logging
setup_logging()

class YouTubeConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video to MP3/MP4 Converter")
        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        # Frame for the header and logo
        header_frame = tk.Frame(self.root, bg="#f0f0f0")
        header_frame.pack(fill="x")

        # Load and display the logo
        logo_image = Image.open("logo.png")
        logo_image = logo_image.resize((200, 100), Image.LANCZOS)  # Use Image.LANCZOS instead of Image.ANTIALIAS
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(header_frame, image=logo_photo, bg="#f0f0f0")
        logo_label.image = logo_photo  # Keep a reference to prevent garbage collection
        logo_label.pack(side="left", padx=10, pady=10)

        title_label = tk.Label(header_frame, text="YouTube Video to MP3/MP4 Converter",
                               font=("Helvetica", 18, "bold"), bg="#f0f0f0")
        title_label.pack(side="left", padx=10)

        # Main content frame
        content_frame = tk.Frame(self.root, padx=20, pady=20)
        content_frame.pack(padx=10, pady=10)

        self.url_label = tk.Label(content_frame, text="YouTube URLs (one per line):", anchor="w")
        self.url_label.grid(row=0, column=0, sticky="w", pady=5)
        self.url_text = tk.Text(content_frame, height=10, width=50, borderwidth=2, relief="solid")
        self.url_text.grid(row=1, column=0, pady=5, columnspan=2)

        self.format_label = tk.Label(content_frame, text="Select Format:", anchor="w")
        self.format_label.grid(row=2, column=0, sticky="w", pady=5)
        self.format_var = tk.StringVar(value="MP4")
        self.format_option = tk.OptionMenu(content_frame, self.format_var, "MP3", "MP4")
        self.format_option.grid(row=2, column=1, pady=5, sticky="ew")

        self.quality_label = tk.Label(content_frame, text="Select Quality (MP4 only):", anchor="w")
        self.quality_label.grid(row=3, column=0, sticky="w", pady=5)
        self.quality_var = tk.StringVar(value="720p")
        self.quality_option = tk.OptionMenu(content_frame, self.quality_var, "720p", "1080p")
        self.quality_option.grid(row=3, column=1, pady=5, sticky="ew")

        self.output_button = tk.Button(content_frame, text="Choose Output Directory", command=self.choose_directory, bg="#007BFF", fg="white")
        self.output_button.grid(row=4, column=0, pady=5)
        self.output_label = tk.Label(content_frame, text="No directory chosen", fg="red", anchor="w")
        self.output_label.grid(row=4, column=1, pady=5, sticky="w")

        self.download_button = tk.Button(content_frame, text="Download", command=self.download_videos, bg="#4CAF50", fg="white")
        self.download_button.grid(row=5, column=0, columnspan=2, pady=20, ipadx=10, ipady=5)

        self.progress = ttk.Progressbar(content_frame, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=6, column=0, columnspan=2, pady=20)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Choose Output Directory", command=self.choose_directory)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def show_about(self):
        about_text = (
            "YouTube Video to MP3/MP4 Converter\n"
            "Version 1.0\n"
            "Author: Martin Hegnum Johannessen\n"
            "GitHub: https://github.com/marhjoh/YoutubeConverterApp"
        )
        messagebox.showinfo("About", about_text)

    def update_progress(self, stream, chunk, bytes_remaining):
        size = stream.filesize
        progress = (size - bytes_remaining) / size * 100
        self.progress['value'] = progress
        self.root.update_idletasks()

    def download_videos(self):
        urls = self.url_text.get("1.0", tk.END).strip().split("\n")
        format = self.format_var.get()
        quality = self.quality_var.get()

        if not urls or not hasattr(self, 'output_path'):
            messagebox.showerror("Error", "Please provide valid URLs and choose an output directory.")
            return

        for url in urls:
            try:
                self.progress['value'] = 0
                download_video(url, format, quality, self.output_path, self.update_progress)
                messagebox.showinfo("Success", f"Download and conversion of {url} completed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred with {url}: {str(e)}")

    def choose_directory(self):
        self.output_path = filedialog.askdirectory()
        if self.output_path:
            self.output_label.config(text=self.output_path, fg="green")
        else:
            self.output_label.config(text="No directory chosen", fg="red")