"""
MystoriumX AI Studio - Cinematic Sound Effects (SFX) Engine
"""
from pathlib import Path
from typing import Dict, List
from config import Config
from utils.logger import setup_logger

logger = setup_logger("SFXEngine")


class SFXEngine:
    """Handles transitional sound effects and thematic audio markers for scenes."""

    def process_sfx(self, scenes: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Maps appropriate sound effect assets to scene transitions."""
        logger.info("Mapping cinematic SFX assets to scenes...")
        processed_scenes = []

        # Look for existing SFX files in assets directory
        sfx_files = list(Config.SFX_DIR.glob("*.mp3")) + list(Config.SFX_DIR.glob("*.wav"))
        default_sfx = str(sfx_files[0]) if sfx_files else ""

        if not sfx_files:
            logger.info("No custom SFX assets found in assets/sfx/. Proceeding with silent SFX markers.")

        for scene in scenes:
            scene_id = scene["scene_id"]
            data = scene.copy()
            
            # Assign transitional SFX marker if available
            data["sfx_path"] = default_sfx
            data["sfx_type"] = "whoosh" if scene_id > 1 else "none"
            
            processed_scenes.append(data)

        logger.info("SFX mapping completed.")
        return processed_scenes
