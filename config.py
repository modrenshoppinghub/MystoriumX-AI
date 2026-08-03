"""
MystoriumX AI Studio - Master Configuration File
"""

import os
from pathlib import Path


class Config:
    # --- Base Paths ---
    BASE_DIR = Path(__file__).resolve().parent
    INPUT_DIR = BASE_DIR / "inputs"
    OUTPUT_DIR = BASE_DIR / "output"

    # --- File Paths (Fixes RAW_SCRIPT AttributeError) ---
    RAW_SCRIPT = INPUT_DIR / "raw_script.txt"
    TEMP_DIR = OUTPUT_DIR / "temp"
    FINAL_VIDEO_DIR = OUTPUT_DIR / "final_video"

    # --- API Keys Configuration ---
    STABILITY_API_KEY = os.getenv("STABILITY_API_KEY", "")

    # --- Image Generation Settings ---
    IMAGE_ENGINE_PROVIDER = (
        "mock"  # Options: "mock", "stability", "pollinations"
    )
    IMAGE_WIDTH = 1920
    IMAGE_HEIGHT = 1080
    STABILITY_ENGINE_ID = "stable-diffusion-v1-6"

    # --- Video & Audio Settings ---
    VIDEO_FPS = 30
    VIDEO_RESOLUTION = (1920, 1080)
    DEFAULT_VOICE = "en-US-ChristopherNeural"
    DEFAULT_WHISPER_MODEL = "base"

    # Audio Ducking Settings (dB)
    VOICE_ATTENUATION_DB = -12.0
    NORMAL_BGM_DB = -4.0


# Ensure directories exist
Config.INPUT_DIR.mkdir(parents=True, exist_ok=True)
Config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
Config.TEMP_DIR.mkdir(parents=True, exist_ok=True)
Config.FINAL_VIDEO_DIR.mkdir(parents=True, exist_ok=True)
