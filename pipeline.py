"""
MystoriumX AI Studio - Complete Master Pipeline Orchestrator
"""

from pathlib import Path
import re
from config import Config
from modules.audio_ducking import AudioDuckingEngine
from modules.image_engine import ImageEngine
from modules.render_engine import RenderEngine
from utils.file_manager import PipelineState
from utils.logger import setup_logger

# --- MoviePy Safe Import ---
try:
    import moviepy.editor as mp
except ImportError:
    import moviepy as mp

logger = setup_logger("Pipeline")


class DocumentaryPipeline:
    """Orchestrates end-to-end automated documentary video creation pipeline"""

    def __init__(self, script_path: Path = None):
        # 1. Ensure output and input directories exist
        if hasattr(Config, "setup_directories"):
            Config.setup_directories()

        # 2. Safe fallback for script path
        if script_path is not None:
            self.script_path = Path(script_path)
        else:
            self.script_path = getattr(
                Config, "RAW_SCRIPT", Config.INPUT_DIR / "raw_script.txt"
            )

        self.state = PipelineState()

        # 3. Initialize Engine Components
        self.image_engine = ImageEngine()
        self.audio_ducking_engine = AudioDuckingEngine(
            voice_attenuation_db=getattr(Config, "VOICE_ATTENUATION_DB", -12.0),
            normal_bgm_db=getattr(Config, "NORMAL_BGM_DB", -4.0),
        )
        self.render_engine = RenderEngine(
            fps=getattr(Config, "VIDEO_FPS", 30),
            resolution=getattr(Config, "VIDEO_RESOLUTION", (1920, 1080)),
        )

    def _parse_script_into_scenes(self, script_text: str) -> list:
        """اسکرپٹ کو جملوں اور مناظر کی بنیاد پر تقسیم کرتا ہے"""
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
        """Runs the complete end-to-end video pipeline"""
        logger.info("🎬 Starting MystoriumX AI Studio Pipeline Run...")

        selected_voice = voice or getattr(
            Config, "DEFAULT_VOICE", "en-US-ChristopherNeural"
        )
        selected_model = whisper_model or getattr(
            Config, "DEFAULT_WHISPER_MODEL", "base"
        )

        # Step 1: Save Script Text if provided directly
        if script_text:
            self.script_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.script_path, "w", encoding="utf-8") as f:
                f.write(script_text.strip())
            logger.info(f"Script written to: {self.script_path}")

        # Step 2: Ensure Script File Exists
        if not self.script_path.exists():
            raise FileNotFoundError(
                f"Script file not found at: {self.script_path}"
            )

        with open(self.script_path, "r", encoding="utf-8") as f:
            raw_script_content = f.read()

        scenes = self._parse_script_into_scenes(raw_script_content)
        logger.info(
            f"Parsed {len(scenes)} scenes/prompts from the raw script."
        )

        temp_dir = getattr(Config, "TEMP_DIR", Config.OUTPUT_DIR / "temp")
        temp_dir.mkdir(parents=True, exist_ok=True)

        # Step 3: Generate Visuals for Each Scene
        image_clips = []
        scene_duration = 5.0  # Default display duration per image in seconds

        for idx, scene_prompt in enumerate(scenes, start=1):
            img_output_path = temp_dir / f"scene_{idx}.png"
            logger.info(f"Generating scene {idx}/{len(scenes)}...")

            # Generate AI image or placeholder using ImageEngine
            saved_img_path = self.image_engine.generate_image(
                prompt=scene_prompt, output_path=img_output_path
            )

            # Create MoviePy ImageClip for each visual
            clip = mp.ImageClip(str(saved_img_path)).set_duration(
                scene_duration
            )
            image_clips.append(clip)

        # Step 4: Define Output Directories and Paths
        final_video_dir = getattr(
            Config, "FINAL_VIDEO_DIR", Config.OUTPUT_DIR / "final_video"
        )
        final_video_dir.mkdir(parents=True, exist_ok=True)
        final_video_path = final_video_dir / "final_documentary.mp4"

        # Step 5: Render Video using RenderEngine
        logger.info("Assembling video clips and exporting final MP4...")
        rendered_path = self.render_engine.export_video(
            video_clips=image_clips,
            audio_path=None,  # Pass mixed audio path here when TTS is enabled
            output_path=final_video_path,
        )

        logger.info(
            f"🚀 Pipeline completed successfully! Video created at: {rendered_path}"
        )
        return rendered_path

    def run(self, *args, **kwargs) -> Path:
        """Alias for app.py compatibility"""
        return self.run_pipeline(*args, **kwargs)
