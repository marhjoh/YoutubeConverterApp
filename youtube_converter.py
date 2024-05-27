import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class YouTubeConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video to MP3/MP4 Converter")
        self.create_widgets()

    def create_widgets(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeConverterApp(root)
    root.mainloop()
