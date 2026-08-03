"""
MystoriumX AI Studio - Edge TTS Voiceover Engine
"""
import asyncio
from pathlib import Path
from typing import Dict, List
import edge_tts
from config import Config
from utils.logger import setup_logger

logger = setup_logger("VoiceEngine")


class VoiceEngine:
    """Generates natural AI documentary voiceovers using Edge-TTS."""

    def __init__(self, voice: str = Config.TTS_VOICE):
        self.voice = voice

    async def _generate_audio_file(self, text: str, output_path: Path):
        """Asynchronously calls edge_tts to synthesize speech to file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(str(output_path))

    def process_narration(self, scenes: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Synthesizes voiceover files for all parsed scenes."""
        logger.info(f"Starting TTS Voice Synthesis (Voice: {self.voice})...")
        processed_scenes = []

        for scene in scenes:
            scene_id = scene["scene_id"]
            audio_path = Config.AUDIO_DIR / f"narration_scene_{scene_id}.mp3"

            logger.info(f"Synthesizing voiceover for Scene {scene_id}...")
            try:
                asyncio.run(self._generate_audio_file(scene["narration"], audio_path))
            except Exception as e:
                logger.error(f"Failed to generate voiceover for Scene {scene_id}: {e}")
                raise e

            data = scene.copy()
            data["narration_audio"] = str(audio_path)
            processed_scenes.append(data)

        logger.info("Voiceover generation completed for all scenes.")
        return processed_scenes
