"""
MystoriumX AI Studio - Module V1: Script & Scene Detection Engine
"""

import json
from pathlib import Path
import re
from config import Config
from utils.logger import setup_logger

logger = setup_logger("ScriptParser")


class ScriptParser:
    """Parses raw text scripts into clean scenes, prompts, and timing estimates."""

    def __init__(self, raw_script_path: Path = None):
        self.raw_script_path = (
            Path(raw_script_path)
            if raw_script_path
            else getattr(Config, "RAW_SCRIPT", None)
        )

    def parse_script(self, script_text: str = None) -> list:
        """Splits raw script into structured scene objects with cinematic prompts."""
        if script_text is None and self.raw_script_path:
            if Path(self.raw_script_path).exists():
                with open(self.raw_script_path, "r", encoding="utf-8") as f:
                    script_text = f.read()

        if not script_text or not script_text.strip():
            raise ValueError("Script text cannot be empty.")

        # Clean whitespace and split by sentence-ending punctuation (English & Urdu)
        cleaned_text = re.sub(r"\s+", " ", script_text.strip())
        sentences = re.split(r"(?<=[.!?۔؟])\s+", cleaned_text)

        scenes = []
        for idx, sentence in enumerate(sentences, start=1):
            sentence = sentence.strip()
            if not sentence:
                continue

            # Estimate duration based on word count (~2.5 words per second for documentary voiceover)
            words = sentence.split()
            estimated_words = len(words)
            estimated_duration = max(3.0, round(estimated_words / 2.5, 2))

            # Generate natural visual prompt hint for AI image generators
            prompt_hint = f"Cinematic documentary scene, high detail, atmospheric lighting: {sentence}"

            scene_data = {
                "scene_id": idx,
                "text": sentence,
                "word_count": estimated_words,
                "estimated_duration_sec": estimated_duration,
                "prompt": prompt_hint,
                "status": "parsed",
            }
            scenes.append(scene_data)

        logger.info(f"V1 Success: Extracted {len(scenes)} scenes from script.")
        return scenes

    def save_parsed_scenes(
        self, scenes: list, output_path: Path = None
    ) -> Path:
        """Saves parsed scenes into a structured JSON file for V2-V10 pipeline."""
        if output_path is None:
            output_path = getattr(
                Config,
                "PARSED_SCENES_JSON",
                Config.OUTPUT_DIR / "temp" / "parsed_scenes.json",
            )

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(scenes, f, ensure_ascii=False, indent=4)

        logger.info(f"Parsed scenes JSON saved to: {output_path}")
        return output_path
