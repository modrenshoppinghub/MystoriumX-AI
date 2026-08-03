"""
MystoriumX AI Studio - Complete Master Pipeline Orchestrator (With Voice & Video)
"""

import asyncio
from pathlib import Path
import re
from config import Config
from modules.audio_ducking import AudioDuckingEngine
from modules.image_engine import ImageEngine
from modules.render_engine import RenderEngine
from utils.file_manager import PipelineState
from utils.logger import setup_logger

# Edge TTS for Natural Free AI Voice
try:
    import edge_tts
except ImportError:
    edge_tts = None

try:
    import moviepy.editor as mp
except ImportError:
    import moviepy as mp

logger = setup_logger("Pipeline")


class DocumentaryPipeline:
    """Orchestrates end-to-end automated documentary video creation pipeline"""

    def __init__(self, script_path: Path = None):
        if hasattr(Config, "setup_directories"):
            Config.setup_directories()

        self.script_path = (
            Path(script_path)
            if script_path
            else getattr(
                Config, "RAW_SCRIPT", Config.INPUT_DIR / "raw_script.txt"
            )
        )
        self.state = PipelineState()

        self.image_engine = ImageEngine()
        self.render_engine = RenderEngine(
            fps=getattr(Config, "VIDEO_FPS", 30),
            resolution=getattr(Config, "VIDEO_RESOLUTION", (1920, 1080)),
        )

    def _generate_audio_voiceover(
        self, text: str, output_audio_path: Path, voice: str
    ):
        """Generates AI Voiceover from text using edge-tts"""
        logger.info(f"Generating AI Voiceover using voice: {voice}...")

        async def _speak():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(str(output_audio_path))

        try:
            asyncio.run(_speak())
            logger.info(f"Voiceover successfully created at: {output_audio_path}")
        except Exception as e:
            logger.error(f"Failed to generate Edge-TTS Voiceover: {e}")

    def _parse_script_into_scenes(self, script_text: str) -> list:
        sentences = re.split(r"(?<=[.!?])\s+", script_text.strip())
        scenes = [s.strip() for s in sentences if s.strip()]
        return scenes if scenes else [script_text]

    def run_pipeline(
        self,
        script_text: str = None,
        voice: str = None,
        whisper_model: str = None,
        **kwargs,
    ) -> Path:
        logger.info("🎬 Starting MystoriumX AI Studio Pipeline Run...")

        selected_voice = voice or getattr(
            Config, "DEFAULT_VOICE", "en-US-ChristopherNeural"
        )

        # 1. Read & Save Script
        if script_text:
            self.script_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.script_path, "w", encoding="utf-8") as f:
                f.write(script_text.strip())

        if not self.script_path.exists():
            raise FileNotFoundError(f"Script file missing: {self.script_path}")

        with open(self.script_path, "r", encoding="utf-8") as f:
            raw_script_content = f.read()

        scenes = self._parse_script_into_scenes(raw_script_content)

        temp_dir = getattr(Config, "TEMP_DIR", Config.OUTPUT_DIR / "temp")
        temp_dir.mkdir(parents=True, exist_ok=True)

        # 2. Generate Voiceover Audio Track
        voice_audio_path = temp_dir / "voiceover.mp3"
        if edge_tts:
            self._generate_audio_voiceover(
                raw_script_content, voice_audio_path, selected_voice
            )

        # Calculate Scene Timings based on Voice
        voice_duration = 10.0
        if voice_audio_path.exists():
            try:
                a_clip = mp.AudioFileClip(str(voice_audio_path))
                voice_duration = a_clip.duration
                a_clip.close()
            except Exception:
                pass

        per_scene_duration = max(3.0, voice_duration / len(scenes))

        # 3. Generate Image Clips
        image_clips = []
        for idx, scene_prompt in enumerate(scenes, start=1):
            img_output_path = temp_dir / f"scene_{idx}.png"
            saved_img_path = self.image_engine.generate_image(
                prompt=scene_prompt, output_path=img_output_path
            )

            clip = mp.ImageClip(str(saved_img_path)).set_duration(
                per_scene_duration
            )
            image_clips.append(clip)

        # 4. Render Final Video
        final_video_dir = getattr(
            Config, "FINAL_VIDEO_DIR", Config.OUTPUT_DIR / "final_video"
        )
        final_video_dir.mkdir(parents=True, exist_ok=True)
        final_video_path = final_video_dir / "final_documentary.mp4"

        rendered_path = self.render_engine.export_video(
            video_clips=image_clips,
            audio_path=(
                voice_audio_path if voice_audio_path.exists() else None
            ),
            output_path=final_video_path,
        )

        logger.info(f"🚀 Video Generation Done: {rendered_path}")
        return rendered_path

    def run(self, *args, **kwargs) -> Path:
        return self.run_pipeline(*args, **kwargs)
