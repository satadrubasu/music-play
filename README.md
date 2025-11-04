
##
yt-dlp (actively maintained fork of youtube-dl) is the usual tool for extracting audio. Example command to download and convert to MP3:

## install (mac/linux)
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

## Python batch downloader

This repository also includes a small Python helper that reads URLs from
`input_urls.txt` and stores the converted MP3 files inside `./output`.

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Ensure `ffmpeg` (and optionally `AtomicParsley` for thumbnail embedding) are
installed and available on your `PATH`:

```bash
brew install ffmpeg atomicparsley
```

### Usage

1. Add one video link per line to `input_urls.txt`. Lines starting with `#` are
  ignored.
2. Run the downloader:

  ```bash
  python download_audio.py
  ```

By default the script mirrors the flags described above: it downloads the best
available audio, converts to MP3, embeds metadata, and attempts to embed the
thumbnail. Output files are saved under `./output`. Use
`python download_audio.py --help` to see additional options such as selecting a
different input list, changing the output directory, disabling thumbnails, or
running in dry-run mode.
