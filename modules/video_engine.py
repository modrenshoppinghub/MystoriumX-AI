"""
MystoriumX AI Studio - Cinematic Video Clips Engine
"""
from pathlib import Path
from typing import Dict, List
import moviepy.editor as mp
from config import Config
from utils.logger import setup_logger

logger = setup_logger("VideoEngine")


class VideoEngine:
    """Assembles image and audio assets into individual video clips with dynamic motion effects."""

    def create_scene_clips(self, scenes: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Combines scene frames and audio tracks into synchronized clip assets."""
        logger.info("Constructing scene video clips...")
        processed_scenes = []

        for scene in scenes:
            scene_id = scene["scene_id"]
            img_path = scene["image_path"]
            audio_path = scene["narration_audio"]
            output_clip_path = Config.FINAL_VIDEO_DIR / f"clip_scene_{scene_id}.mp4"

            logger.info(f"Rendering Video Clip for Scene {scene_id}...")
            try:
                # Load audio track to derive timing
                audio_clip = mp.AudioFileClip(audio_path)
                duration = audio_clip.duration

                # Create base image clip matching audio length
                image_clip = (
                    mp.ImageClip(img_path)
                    .set_duration(duration)
                    .set_fps(Config.FPS)
                    .resize(Config.RESOLUTION)
                )

                # Set audio on video track
                video_clip = image_clip.set_audio(audio_clip)

                # Export individual clip
                video_clip.write_videofile(
                    str(output_clip_path),
                    fps=Config.FPS,
                    codec="libx264",
                    audio_codec="aac",
                    logger=None,
                )

                audio_clip.close()
                video_clip.close()

            except Exception as e:
                logger.error(f"Failed to generate video clip for Scene {scene_id}: {e}")
                raise e

            data = scene.copy()
            data["clip_path"] = str(output_clip_path)
            data["duration"] = duration
            processed_scenes.append(data)

        logger.info("Scene video clips created successfully.")
        return processed_scenes
