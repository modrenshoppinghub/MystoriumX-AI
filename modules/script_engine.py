"""
MystoriumX AI Studio - Script Processing Engine
"""
import re
from pathlib import Path
from typing import Dict, List
from utils.helpers import clean_text
from utils.logger import setup_logger

logger = setup_logger("ScriptEngine")


class ScriptEngine:
    """Handles text script loading, cleaning, and dynamic scene segmentation."""

    def __init__(self, script_path: Path):
        self.script_path = script_path

    def load_and_parse(self) -> List[Dict[str, str]]:
        """Reads raw script text file and splits it into structured logical scenes."""
        if not self.script_path.exists():
            error_msg = f"Script file not found at path: {self.script_path}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)

        logger.info(f"Loading script from {self.script_path}...")
        with open(self.script_path, "r", encoding="utf-8") as f:
            raw_text = f.read().strip()

        if not raw_text:
            error_msg = "Script file is empty."
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Split script by explicit scene markers [SCENE], numbers, or double line breaks
        raw_scenes = re.split(r'\n\s*\n|\[SCENE\s*\d*\]', raw_text)
        scenes = []

        scene_counter = 1
        for block in raw_scenes:
            cleaned = clean_text(block)
            if cleaned:
                scenes.append({
                    "scene_id": scene_counter,
                    "narration": cleaned
                })
                scene_counter += 1

        logger.info(f"Script successfully parsed into {len(scenes)} distinct scenes.")
        return scenes
