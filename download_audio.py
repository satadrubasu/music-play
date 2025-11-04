#!/usr/bin/env python3
"""Batch audio downloader powered by yt-dlp.

Reads video URLs from a text file and saves MP3 files into an output directory.
Configuration mirrors the CLI example from the README, including metadata and
thumbnail embedding support.
"""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from pathlib import Path
from typing import Iterable, Iterator, Tuple

import yt_dlp
from yt_dlp.utils import DownloadError

LOGGER = logging.getLogger("yt_audio_downloader")


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download and convert audio from a list of video URLs.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("input_urls.txt"),
        help="Path to the text file containing one URL per line (default: input_urls.txt).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Directory where the MP3 files will be written (default: ./output).",
    )
    parser.add_argument(
        "--audio-format",
        default="mp3",
        help="Target audio format (default: mp3).",
    )
    parser.add_argument(
        "--audio-quality",
        default="0",
        help="FFmpeg quality value passed to yt-dlp (default: 0 = best).",
    )
    parser.add_argument(
        "--skip-thumbnail",
        action="store_true",
        help="Do not download and embed thumbnails.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print the videos that would be processed without downloading.",
    )
    return parser.parse_args(argv)


def load_urls(path: Path) -> Iterator[Tuple[int, str]]:
    """Yield (line_number, url) pairs, skipping blanks and comments."""
    if not path.exists():
        raise FileNotFoundError(f"URL list not found: {path}")

    with path.open("r", encoding="utf-8") as handle:
        for idx, raw_line in enumerate(handle, start=1):
            url = raw_line.strip()
            if not url or url.startswith("#"):
                continue
            yield idx, url


def ensure_external_tools() -> None:
    """Warn the operator if ffmpeg or atomicparsley are missing."""
    if shutil.which("ffmpeg") is None:
        LOGGER.warning(
            "ffmpeg is not on PATH; audio conversion will fail. "
            "Install it via Homebrew: brew install ffmpeg"
        )
    if shutil.which("AtomicParsley") is None:
        LOGGER.warning(
            "AtomicParsley is not on PATH; thumbnail embedding might fail. "
            "Install it via Homebrew: brew install atomicparsley"
        )


def build_ydl_options(args: argparse.Namespace, output_dir: Path) -> dict:
    template = output_dir / "%(title)s.%(ext)s"
    postprocessors = [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": args.audio_format,
            "preferredquality": args.audio_quality,
        },
        {"key": "FFmpegMetadata"},
    ]

    opts = {
        "format": "bestaudio/best",
        "outtmpl": str(template),
        "postprocessors": postprocessors,
        "postprocessor_args": ["-id3v2_version", "3"],
        "ignoreerrors": False,
        "noprogress": False,
        "quiet": False,
        "restrictfilenames": False,
        "writethumbnail": not args.skip_thumbnail,
        "embedthumbnail": not args.skip_thumbnail,
    }

    if not args.skip_thumbnail:
        postprocessors.append({"key": "EmbedThumbnail"})

    return opts


def download_from_list(args: argparse.Namespace) -> int:
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    ensure_external_tools()

    if args.dry_run:
        LOGGER.info("Dry run enabled; no files will be downloaded.")

    try:
        entries = list(load_urls(args.input))
    except FileNotFoundError as exc:
        LOGGER.error("%s", exc)
        return 1

    if not entries:
        LOGGER.warning("No URLs found in %s", args.input)
        return 0

    opts = build_ydl_options(args, output_dir)

    failures = 0
    for line_no, url in entries:
        LOGGER.info("Processing line %d: %s", line_no, url)
        if args.dry_run:
            continue
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
        except DownloadError as err:
            failures += 1
            LOGGER.error("Failed to download line %d (%s): %s", line_no, url, err)
        except Exception:  # noqa: BLE001 - capture unexpected errors per URL
            failures += 1
            LOGGER.exception("Unexpected error on line %d (%s)", line_no, url)

    if failures:
        LOGGER.error("Completed with %d failures", failures)
        return 1

    LOGGER.info("All downloads completed successfully.")
    return 0


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
    )


def main(argv: Iterable[str] | None = None) -> int:
    configure_logging()
    args = parse_args(argv)

    try:
        return download_from_list(args)
    except KeyboardInterrupt:
        LOGGER.warning("Interrupted by user.")
        return 130


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    sys.exit(main())
