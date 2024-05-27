import re
import logging

def setup_logging():
    """
    Setup logging configuration.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )

def validate_url(url):
    """
    Validate the given YouTube URL.

    Args:
        url (str): The YouTube URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    youtube_regex = re.compile(
        r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
    )
    return re.match(youtube_regex, url) is not None