"""
MystoriumX AI Studio - Final Video Rendering Engine
"""
from pathlib import Path
from typing import Dict, List
import moviepy.editor as mp
from config import Config
from utils.logger import setup_logger

logger = setup_logger("RenderEngine")


class RenderEngine:
    """Combines scene video clips, audio tracks, and transitions into a complete documentary."""

    def render_final_video(
        self, scenes: List[Dict[str, str]], mastered_audio_path: Path
    ) -> Path:
        """Stitches clips into a single video file and syncs with mastered audio."""
        output_video_path = Config.FINAL_VIDEO_DIR / "final_documentary.mp4"
        logger.info("Assembling final video timeline...")

        try:
            clips = []
            for scene in scenes:
                clip_path = scene["clip_path"]
                clip = mp.VideoFileClip(clip_path)

                # Add crossfade transition effect if scene isn't the first
                if len(clips) > 0:
                    clip = clip.crossfadein(Config.CROSSFADE_DURATION)

                clips.append(clip)

            logger.info("Concatenating video scenes...")
            concatenated = mp.concatenate_videoclips(clips, method="compose")

            # Attach final ducked and mastered audio track
            master_audio = mp.AudioFileClip(str(mastered_audio_path))
            final_video = concatenated.set_audio(master_audio)

            logger.info(f"Rendering output file to {output_video_path} (FPS: {Config.FPS})...")
            final_video.write_videofile(
                str(output_video_path),
                fps=Config.FPS,
                codec=Config.VIDEO_CODEC,
                audio_codec=Config.AUDIO_CODEC,
                threads=4,
                logger=None,
            )

            # Cleanup open file handles
            for clip in clips:
                clip.close()
            final_video.close()
            master_audio.close()

            logger.info(f"Rendering complete! Master video saved at: {output_video_path}")
            return output_video_path

        except Exception as e:
            logger.error(f"Error rendering final video pipeline: {e}")
            raise e
