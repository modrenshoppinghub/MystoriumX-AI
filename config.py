"""
MystoriumX AI Studio - Global Configuration Manager
"""
import os
from pathlib import Path


class Config:
    # Root Directory Paths
    BASE_DIR = Path(__file__).resolve().parent
    INPUT_DIR = BASE_DIR / "input"
    OUTPUT_DIR = BASE_DIR / "output"
    ASSETS_DIR = BASE_DIR / "assets"

    # Google Drive Mount Path for Colab Environment
    DRIVE_MOUNT_PATH = Path("/content/drive/MyDrive/MystoriumX_Studio_Output")

    # Input Files Paths
    SCRIPT_PATH = INPUT_DIR / "script.txt"
    SETTINGS_PATH = INPUT_DIR / "settings.json"
    STATE_FILE = OUTPUT_DIR / "pipeline_state.json"

    # Output Sub-directories
    AUDIO_DIR = OUTPUT_DIR / "audio"
    IMAGE_DIR = OUTPUT_DIR / "images"
    SUBTITLE_DIR = OUTPUT_DIR / "subtitles"
    THUMBNAIL_DIR = OUTPUT_DIR / "thumbnail"
    FINAL_VIDEO_DIR = OUTPUT_DIR / "final_video"

    # Assets Sub-directories
    FONTS_DIR = ASSETS_DIR / "fonts"
    MUSIC_DIR = ASSETS_DIR / "music"
    SFX_DIR = ASSETS_DIR / "sfx"
    LOGO_DIR = ASSETS_DIR / "logo"

    # Default Render Configurations
    FPS = 30
    RESOLUTION = (1920, 1080)  # 16:9 Standard Documentary Resolution (Width, Height)
    FONT_PATH = FONTS_DIR / "Cinematic.ttf"

    # AI Engine Models & TTS Configurations
    WHISPER_MODEL_SIZE = "small"
    TTS_VOICE = "en-US-ChristopherNeural"  # Deep Narrative Documentary Voice

    @classmethod
    def initialize_directories(cls):
        """Ensures all necessary project directories exist before runtime."""
        directories = [
            cls.INPUT_DIR,
            cls.OUTPUT_DIR,
            cls.ASSETS_DIR,
            cls.AUDIO_DIR,
            cls.IMAGE_DIR,
            cls.SUBTITLE_DIR,
            cls.THUMBNAIL_DIR,
            cls.FINAL_VIDEO_DIR,
            cls.FONTS_DIR,
            cls.MUSIC_DIR,
            cls.SFX_DIR,
            cls.LOGO_DIR,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
