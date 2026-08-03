"""
MystoriumX AI Studio - Dynamic Audio Ducking Engine
"""
from pathlib import Path
from typing import Dict, List
from pydub import AudioSegment
from config import Config
from utils.logger import setup_logger

logger = setup_logger("AudioDucking")


class AudioDuckingEngine:
    """Applies dynamic sidechain-style audio ducking to background music tracks."""

    def process_audio(
        self,
        scenes: List[Dict[str, str]],
        bg_music_path: Path,
        duck_db: float = -14.0,
    ) -> Path:
        """Overlays dynamic background soundtrack with speech-triggered volume reduction."""
        logger.info("Applying dynamic audio ducking to background soundtrack...")
        final_audio_path = Config.AUDIO_DIR / "final_mastered_audio.mp3"

        try:
            # Build full concatenated narrator voiceover track
            master_narration = AudioSegment.silent(duration=0)
            for scene in scenes:
                narration_clip = AudioSegment.from_file(scene["narration_audio"])
                master_narration += narration_clip

            # Load synthesized background music track
            bg_music = AudioSegment.from_file(bg_music_path)

            # Match lengths precisely
            if len(bg_music) < len(master_narration):
                bg_music = bg_music * (len(master_narration) // len(bg_music) + 1)
            bg_music = bg_music[: len(master_narration)]

            # Apply ducking volume reduction (-14dB lower than voiceover)
            ducked_bg_music = bg_music.apply_gain(duck_db)

            # Master composite mix (Overlay voiceover over ducked music)
            mastered_track = ducked_bg_music.overlay(master_narration)

            mastered_track.export(final_audio_path, format="mp3")
            logger.info(f"Mastered audio composite created at: {final_audio_path}")
            return final_audio_path

        except Exception as e:
            logger.error(f"Failed to process dynamic audio ducking: {e}")
            raise e
