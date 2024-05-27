import tkinter as tk
from tkinter import filedialog, messagebox, ttk

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

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeConverterApp(root)
    root.mainloop()
