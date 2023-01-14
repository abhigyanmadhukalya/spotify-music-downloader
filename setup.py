from importlib.metadata import requires
from setuptools import setup

requires = [
    "flask",
    "spotipy",
    "html5lib",
    "requests",
    "requests-html",
    "beautifulsoup4",
    "youtube_dl",
    "pathlib",
    "pandas",
]

setup(
    name="Spotify-Playlist-Downloader",
    version="1.0",
    description="Download Spotify playlists to mp3",
    author="Abhigyan Madhukalya",
    author_email="amadhukalya2005@gmail.com",
    keywords="spotify playlist downloader mp3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
