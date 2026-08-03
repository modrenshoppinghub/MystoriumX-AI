"""
MystoriumX AI Studio - Automated Subtitle & Transcription Engine
"""
from pathlib import Path
from typing import Dict, List
import whisper
from config import Config
from utils.logger import setup_logger

logger = setup_logger("SubtitleEngine")


class SubtitleEngine:
    """Generates accurate frame-accurate SRT subtitles using OpenAI Whisper models."""

    def __init__(self, model_size: str = Config.WHISPER_MODEL_SIZE):
        self.model_size = model_size
        self._model = None

    def _load_model(self):
        """Lazy loads Whisper model into RAM/VRAM."""
        if self._model is None:
            logger.info(f"Loading Whisper model ({self.model_size})...")
            self._model = whisper.load_model(self.model_size)

    def _format_timestamp(self, seconds: float) -> str:
        """Converts raw float seconds to standard SRT format HH:MM:SS,mmm."""
        millis = int((seconds % 1) * 1000)
        secs = int(seconds) % 60
        mins = (int(seconds) // 60) % 60
        hrs = int(seconds) // 3600
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

    def generate_subtitles(self, scenes: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Transcribes individual scene audio files and creates consolidated SRT subtitle assets."""
        self._load_model()
        logger.info("Generating SRT subtitle transcripts...")

        srt_path = Config.SUBTITLE_DIR / "full_documentary.srt"
        srt_lines = []
        global_index = 1
        time_offset = 0.0

        processed_scenes = []

        for scene in scenes:
            audio_path = scene["narration_audio"]
            duration = scene.get("duration", 0.0)

            logger.info(f"Transcribing audio segment for Scene {scene['scene_id']}...")
            result = self._model.transcribe(audio_path, word_timestamps=True)

            scene_subtitles = []
            for segment in result.get("segments", []):
                start = segment["start"] + time_offset
                end = segment["end"] + time_offset
                text = segment["text"].strip()

                srt_entry = f"{global_index}\n{self._format_timestamp(start)} --> {self._format_timestamp(end)}\n{text}\n"
                srt_lines.append(srt_entry)

                scene_subtitles.append({
                    "start": start,
                    "end": end,
                    "text": text
                })
                global_index += 1

            time_offset += duration
            data = scene.copy()
            data["subtitles"] = scene_subtitles
            processed_scenes.append(data)

        # Write combined SRT file
        srt_path.parent.mkdir(parents=True, exist_ok=True)
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write("\n".join(srt_lines))

        logger.info(f"Subtitle generation finished. Exported to: {srt_path}")
        return processed_scenes
