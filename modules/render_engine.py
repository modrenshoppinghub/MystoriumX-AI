"""
MystoriumX AI Studio - Master Render Engine
"""

from pathlib import Path
from utils.logger import setup_logger

try:
    import moviepy.editor as mp
except ImportError:
    import moviepy as mp

logger = setup_logger("RenderEngine")


class RenderEngine:
    """Combines Visuals, Voiceover, and Audio to render final MP4 video"""

    def __init__(self, fps: int = 30, resolution: tuple = (1920, 1080)):
        self.fps = fps
        self.resolution = resolution

    def export_video(
        self,
        video_clips: list,
        audio_path: Path = None,
        output_path: Path = None,
    ) -> Path:
        """Assembles image clips and audio into a final video MP4 file"""
        if not video_clips:
            raise ValueError("No video clips provided for rendering.")

        logger.info(
            f"Concatenating {len(video_clips)} clips for video rendering..."
        )
        final_clip = mp.concatenate_videoclips(video_clips, method="compose")

        # Attach voiceover audio if present
        if audio_path and Path(audio_path).exists():
            logger.info(f"Attaching audio track from: {audio_path}")
            audio_clip = mp.AudioFileClip(str(audio_path))

            # Adjust video length to match exact voiceover duration
            final_clip = final_clip.set_duration(audio_clip.duration)
            final_clip = final_clip.set_audio(audio_clip)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Rendering final MP4 to: {output_path}")
        final_clip.write_videofile(
            str(output_path),
            fps=self.fps,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            threads=4,
        )

        return output_path
