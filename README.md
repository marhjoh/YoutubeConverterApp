# YouTube Video to MP3/MP4 Converter

A simple Python application to download and convert YouTube videos to MP3 or MP4 format, featuring a graphical user interface (GUI) for ease of use.

## Features

- Convert YouTube videos to MP3.
- Convert YouTube videos to MP4.
- Batch processing of multiple videos.
- Option to choose the quality of the output file (e.g., 720p, 1080p for video, bitrate for audio).
- Simple graphical user interface (GUI) for user interaction.
- Download progress indicator.
- Error handling and input validation.
- Option to choose the storage location on your computer.

## Installation

1. **Clone the Repository:**

    ```sh
    git clone https://github.com/marhjoh/YoutubeConverterApp.git
    cd YoutubeConverterApp
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the required dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the application:**

    ```sh
    python main.py
    ```

2. **Using the GUI:**
    - Enter YouTube URLs (one per line) in the text area.
    - Select the desired format (MP3 or MP4).
    - If MP4 is selected, choose the quality (720p or 1080p).
    - Choose the output directory where the files will be saved.
    - Click "Download" to start downloading and converting the videos.

## Common Issues

### HTTP Error 400: Bad Request

This error typically indicates that there is an issue with the URL being passed to the YouTube API. Here are some potential causes and solutions:

1. **Invalid URL Format:**
    - Ensure the URL is correctly formatted and valid.
    - Use the clean URL function to remove unnecessary parameters from the URL.

2. **URL with Playlist or Additional Parameters:**
    - If the URL contains a playlist or other additional parameters, it might not be handled correctly by `pytube`.
    - The application includes a function to clean the URL, ensuring it only contains the video ID parameter.

3. **API Restrictions or Quotas:**
    - There might be restrictions or quotas on the YouTube API usage.
    - Ensure that the requests are not exceeding any limits.

4. **Unsupported Video Types:**
    - Some videos might be restricted or not supported for download by `pytube`.
    - Check if the video is available for public viewing and not restricted.

To address these issues, the application uses a `clean_url` function to ensure the URL is correctly formatted before being processed.

## Development

### Code Structure

- `main.py`: Initializes the application and creates the main window.
- `gui.py`: Contains the GUI logic for the application.
- `downloader.py`: Contains the core logic for downloading and converting videos.
- `utils.py`: utility function for logging.