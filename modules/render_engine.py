"""
MystoriumX AI Studio - Final Video Render Engine
"""

from pathlib import Path
from utils.logger import setup_logger

# --- MoviePy Version Compatibility Patch ---
try:
    import moviepy.editor as mp
except ImportError:
    import moviepy as mp
# -------------------------------------------

logger = setup_logger("RenderEngine")


class RenderEngine:

    def __init__(self, fps: int = 30, resolution: tuple = (1920, 1080)):
        self.fps = fps
        self.resolution = resolution

    def export_video(
        self, video_clips: list, audio_path: Path, output_path: Path
    ) -> Path:
        """تمام ویڈیو کلپس اور مکسڈ آڈیو کو ملا کر 1080p MP4 ایکسپورٹ کرتا ہے"""
        logger.info(
            f"Assembling {len(video_clips)} clips into final documentary..."
        )

        try:
            # ویڈیو کلپس کو یکجا کریں
            final_clip = mp.concatenate_videoclips(
                video_clips, method="compose"
            )

            # آڈیو اٹیچ کریں
            if audio_path and audio_path.exists():
                audio_clip = mp.AudioFileClip(str(audio_path))
                final_clip = final_clip.set_audio(audio_clip)

            output_path.parent.mkdir(parents=True, exist_ok=True)

            # MP4 رینڈر کریں
            final_clip.write_videofile(
                str(output_path),
                fps=self.fps,
                codec="libx264",
                audio_codec="aac",
                logger=None,  # Suppress moviepy stdout logs
            )

            logger.info(f"Final video successfully exported to: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to render video: {e}")
            raise e
