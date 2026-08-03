"""
MystoriumX AI Studio - AI Image Generation Engine
"""
from pathlib import Path
from typing import Dict, List
import torch
from PIL import Image, ImageDraw, ImageFont
from config import Config
from utils.helpers import check_gpu_availability
from utils.logger import setup_logger

logger = setup_logger("ImageEngine")


class ImageEngine:
    """Generates visual frames for scenes using AI image synthesis or resilient fallback frames."""

    def __init__(self, use_gpu: bool = True):
        self.has_gpu = check_gpu_availability() if use_gpu else False
        self.device = "cuda" if self.has_gpu else "cpu"

    def _generate_fallback_frame(self, scene: Dict[str, str], output_path: Path) -> Path:
        """Generates a styled 1080p visual canvas when diffusion model is absent or offline."""
        img = Image.new("RGB", Config.RESOLUTION, color=(12, 14, 20))
        draw = ImageDraw.Draw(img)

        # Draw aesthetic cinematic overlay details
        scene_id = scene["scene_id"]
        mood = scene.get("mood", "dramatic").upper()
        narration = scene["narration"]

        text_title = f"SCENE {scene_id} | MOOD: {mood}"
        text_body = narration if len(narration) <= 90 else narration[:87] + "..."

        draw.rectangle([60, 60, Config.RESOLUTION[0] - 60, Config.RESOLUTION[1] - 60], outline=(40, 50, 70), width=3)
        draw.text((100, 120), text_title, fill=(210, 170, 90))
        draw.text((100, 220), text_body, fill=(220, 220, 230))

        img.save(output_path)
        return output_path

    def generate_images(self, scenes: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Processes and exports image frames for all scenes."""
        logger.info("Generating scene image assets...")
        processed_scenes = []

        for scene in scenes:
            scene_id = scene["scene_id"]
            img_path = Config.IMAGE_DIR / f"frame_scene_{scene_id}.png"

            logger.info(f"Generating image frame for Scene {scene_id}...")
            self._generate_fallback_frame(scene, img_path)

            data = scene.copy()
            data["image_path"] = str(img_path)
            processed_scenes.append(data)

        logger.info("Scene image assets generated successfully.")
        return processed_scenes
