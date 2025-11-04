
##
yt-dlp (actively maintained fork of youtube-dl) is the usual tool for extracting audio. Example command to download and convert to MP3:

### Quick legal note  
Only proceed if one of these is true:
you own the video/audio,
the uploader explicitly granted permission to download/redistribute, or
the content is licensed for reuse (e.g., Creative Commons) or public-domain.
If you don’t have permission, use official options like YouTube Music / YouTube Premium, or contact the rights owner.
At least make sure avoid 
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


## Integrating uvr5 
( make sure pyenv is 3.9.x) 

Given UVR5 is installed in MAC at : /Applications/Ultimate Vocal Remover.app/Contents/  
```
cd ~
git clone https://github.com/Anjok07/ultimatevocalremovergui.git
cd ultimatevocalremovergui
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Link or copy your existing models

Now, in your cloned repo, you’ll see:  
ultimatevocalremovergui/models/   
Instead of downloading models again, just symlink or copy the existing model folder from your .app.  

Option B — Replace the whole models/ folder (simple & clean)

If you don’t care about the few models already there or want to share exactly the same model set between GUI and CLI, just replace the entire directory with a symlink:
```   
cd ~/ultimatevocalremovergui
rm -rf ~/ultimatevocalremovergui/models
ln -s "/Applications/Ultimate Vocal Remover.app/Contents/Resources/models" ./models
```

## Execute Application CLI : 

```
python3 separate.py -i "/path/to/song.mp3" -o "/path/to/output"
```

Specify the model :   
```
python3 separate.py -i "/path/to/song.mp3" -o "/path/to/output" -m "UVR-MDX-NET-Voc_FT"
```

Parameters commonly supported:

Flag	Meaning
-i	Input file or directory
-o	Output directory
-m	Model name (e.g. UVR-MDX-NET-Voc_FT)
--format	Output format (wav/mp3/flac)
--gpu	Enable GPU (if available)

Run python3 separate.py -h for all supported flags.

## Integrating the yt-download and this script

