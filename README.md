Automated, legal workflow (using yt-dlp)

yt-dlp (actively maintained fork of youtube-dl) is the usual tool for extracting audio. Example command to download and convert to MP3:

# install (mac/linux)
brew install yt-dlp            # or: pip install -U yt-dlp

# download and convert to MP3 (best quality), add metadata and embed thumbnail
yt-dlp -x \
  --audio-format mp3 \
  --audio-quality 0 \
  --add-metadata \
  --embed-thumbnail \
  -o '%(title)s.%(ext)s' \
  "YOUTUBE_URL_HERE"


Flags explained:

-x : extract audio only
--audio-format mp3 : convert to MP3
--audio-quality 0 : best audio quality for conversion
--add-metadata : add video metadata (title/artist/date) into file tags
--embed-thumbnail : embed thumbnail as cover art
-o '%(title)s.%(ext)s' : output filename template
