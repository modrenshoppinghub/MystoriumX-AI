"""
MystoriumX AI Studio - Ambient & Background Music Engine
"""
from pathlib import Path
from typing import Dict, List
from pydub import AudioSegment
from pydub.generators import Sine
from config import Config
from utils.logger import setup_logger

logger = setup_logger("MusicEngine")


class MusicEngine:
    """Generates dynamic ambient music or composites cinematic atmospheric stems."""

    def generate_ambient_track(self, scenes: List[Dict[str, str]], total_duration_sec: float) -> Path:
        """Generates procedural atmospheric background music matching the documentary length."""
        output_path = Config.AUDIO_DIR / "background_music.mp3"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Generating cinematic background soundtrack ({total_duration_sec:.1f}s)...")

        try:
            # Check if custom music track exists in assets/music/
            custom_music = list(Config.MUSIC_DIR.glob("*.mp3")) + list(Config.MUSIC_DIR.glob("*.wav"))
            if custom_music:
                logger.info(f"Found existing custom soundtrack: {custom_music[0].name}")
                track = AudioSegment.from_file(custom_music[0])
                # Loop track to match video length
                target_ms = int(total_duration_sec * 1000)
                looped = track
                while len(looped) < target_ms:
                    looped += track
                final_music = looped[:target_ms].fade_in(2000).fade_out(3000)
            else:
                logger.info("No custom audio stem found. Synthesizing low ambient drone pad...")
                # Procedural low-frequency atmospheric drone pad (A Minor drone base)
                pad = Sine(110).to_audio_segment(duration=int(total_duration_sec * 1000)).low_pass_filter(220)
                final_music = pad - 22  # Duck volume down to background levels (-22dB)

            final_music.export(output_path, format="mp3")
            logger.info(f"Background music created successfully at: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error producing background soundtrack: {e}")
            raise e
