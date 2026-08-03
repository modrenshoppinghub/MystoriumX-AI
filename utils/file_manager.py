"""
MystoriumX AI Studio - Pipeline State & File Manager
"""

import json
from pathlib import Path
from config import Config
from utils.logger import setup_logger

logger = setup_logger("FileManager")


class PipelineState:
    """Tracks and manages pipeline state across process steps"""

    def __init__(self, state_file: Path = None):
        if state_file is not None:
            self.state_file = Path(state_file)
        else:
            self.state_file = getattr(
                Config, "STATE_FILE", Config.OUTPUT_DIR / "pipeline_state.json"
            )

        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state = self.load_state()

    def load_state(self) -> dict:
        """Loads state from JSON file or returns default state"""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load pipeline state: {e}")

        return {
            "status": "idle",
            "current_step": "init",
            "script_loaded": False,
            "voice_generated": False,
            "images_generated": False,
            "video_rendered": False,
        }

    def save_state(self, updated_data: dict = None):
        """Saves current state dictionary to JSON file"""
        if updated_data:
            self.state.update(updated_data)

        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(self.state, f, indent=4)
            logger.info(f"Pipeline state saved to: {self.state_file}")
        except Exception as e:
            logger.error(f"Failed to save pipeline state: {e}")
