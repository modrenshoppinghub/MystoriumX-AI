"""
MystoriumX AI Studio - Asset and Model Downloader Module
"""
import urllib.request
from pathlib import Path
from utils.logger import setup_logger

logger = setup_logger("Downloader")


def download_file(url: str, output_path: Path) -> Path:
    """Downloads a file from a URL to a specified local path with progress feedback."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists():
        logger.info(f"File already exists: {output_path.name}. Skipping download.")
        return output_path

    logger.info(f"Downloading from {url} to {output_path}...")
    try:
        urllib.request.urlretrieve(url, output_path)
        logger.info(f"Successfully downloaded: {output_path.name}")
        return output_path
    except Exception as e:
        logger.error(f"Failed to download file from {url}: {e}")
        raise e


def ensure_default_font(font_path: Path) -> Path:
    """Ensures a default cinematic TTF font exists in assets/fonts/."""
    if font_path.exists():
        return font_path

    # Fallback default open-source Roboto font URL
    default_font_url = "https://github.com/google/fonts/raw/main/ofl/roboto/Roboto-Bold.ttf"
    logger.info("Cinematic font not found. Downloading default fallback font...")
    return download_file(default_font_url, font_path)
