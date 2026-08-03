"""
MystoriumX AI Studio - Scene Mood and Context Analysis Engine
"""
from typing import Dict, List
from utils.logger import setup_logger

logger = setup_logger("SceneDetector")


class SceneDetector:
    """Analyzes scene narration to determine cinematic tone, mood, and visual markers."""

    MOOD_KEYWORDS = {
        "mysterious": ["dark", "ancient", "secret", "unknown", "hidden", "shadow", "fog", "deep", "abyss", "lost"],
        "dramatic": ["war", "battle", "clash", "explosion", "crisis", "fall", "death", "power", "empire", "blood"],
        "inspirational": ["future", "light", "rise", "victory", "hope", "discovery", "gold", "golden", "triumph", "dream"],
        "suspenseful": ["silence", "danger", "stalk", "creepy", "night", "trap", "fear", "ghost", "stalking", "unseen"]
    }

    def analyze_scenes(self, scenes: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Applies keyword sentiment and mood detection to each scene."""
        logger.info("Analyzing tone and mood for all scenes...")
        processed_scenes = []

        for scene in scenes:
            narration_lower = scene["narration"].lower()
            detected_mood = "dramatic"  # Default cinematic baseline

            for mood, keywords in self.MOOD_KEYWORDS.items():
                if any(keyword in narration_lower for keyword in keywords):
                    detected_mood = mood
                    break

            data = scene.copy()
            data["mood"] = detected_mood
            processed_scenes.append(data)

        logger.info("Scene mood detection completed.")
        return processed_scenes
