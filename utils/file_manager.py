"""
MystoriumX AI Studio - State & File Management Module
"""
import json
import shutil
from pathlib import Path
from typing import Any, Dict
from config import Config
from utils.logger import setup_logger

logger = setup_logger("FileManager")


class PipelineState:
    """Manages pipeline execution state, allowing resume functionality across stages."""

    def __init__(self, state_file: Path = Config.STATE_FILE):
        self.state_file = state_file
        self.state = self.load_state()

    def load_state(self) -> Dict[str, Any]:
        """Loads state from JSON file if exists, else returns empty dict."""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load pipeline state: {e}")
        return {}

    def update_stage(self, stage_name: str, data: Any):
        """Updates and saves the state for a completed stage."""
        self.state[stage_name] = {
            "status": "COMPLETED",
            "data": data,
        }
        self.save()

    def is_completed(self, stage_name: str) -> bool:
        """Checks if a stage is already marked as completed."""
        return self.state.get(stage_name, {}).get("status") == "COMPLETED"

    def get_stage_data(self, stage_name: str) -> Any:
        """Retrieves data saved from a previous stage."""
        return self.state.get(stage_name, {}).get("data")

    def save(self):
        """Writes current state to disk as JSON."""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(self.state, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save pipeline state: {e}")


def cleanup_temp_files(directory: Path):
    """Deletes temporary generated assets inside a directory."""
    if directory.exists() and directory.is_dir():
        for file in directory.glob("*"):
            try:
                if file.is_file():
                    file.unlink()
                elif file.is_dir():
                    shutil.rmtree(file)
            except Exception as e:
                logger.warning(f"Could not delete temp file {file}: {e}")
        logger.info(f"Cleaned up directory: {directory}")
