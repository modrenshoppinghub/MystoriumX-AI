"""
MystoriumX AI Studio - Helper & Hardware Utilities Module
"""
import re
import torch
from utils.logger import setup_logger

logger = setup_logger("Helpers")


def check_gpu_availability() -> bool:
    """Checks if CUDA GPU is available and logs hardware information."""
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        logger.info(f"GPU Detected: {gpu_name} (CUDA Enabled)")
        return True
    else:
        logger.warning("No GPU detected. Pipeline will run in CPU mode (Slower).")
        return False


def clean_text(text: str) -> str:
    """Cleans script text by removing special characters and extra spaces."""
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def format_seconds_to_time(seconds: float) -> str:
    """Converts seconds into HH:MM:SS format."""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hrs:02d}:{mins:02d}:{secs:02d}"
