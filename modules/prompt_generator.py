"""
MystoriumX AI Studio - Cinematic Visual Prompt Generator
"""
from typing import Dict, List
from utils.logger import setup_logger

logger = setup_logger("PromptGenerator")


class PromptGenerator:
    """Translates scene narration and mood into optimized AI diffusion prompts."""

    STYLE_PRESETS = {
        "mysterious": (
            "cinematic documentary shot, dark foggy atmosphere, hyperrealistic 8k, "
            "volumetric cinematic lighting, epic composition, unreal engine 5 render, highly detailed, photorealistic"
        ),
        "dramatic": (
            "cinematic action shot, intense dramatic lighting, historical realism, "
            "high contrast, 35mm film print style, octane render, masterwork, masterpiece, 8k resolution"
        ),
        "inspirational": (
            "glorious golden hour lighting, cinematic panoramic shot, highly detailed photorealistic, "
            "uplifting atmosphere, 8k resolution, vivid colors, masterwork"
        ),
        "suspenseful": (
            "shadowy film noir aesthetic, subtle tension, low key lighting, cold color palette, "
            "photorealistic 8k, highly detailed, dramatic shadows, cinematic framing"
        )
    }

    NEGATIVE_PROMPT = (
        "blurry, low quality, distorted, cartoon, anime, illustration, text, watermark, "
        "bad anatomy, overexposed, ugly, extra limbs, bad proportions"
    )

    def generate_prompts(self, scenes: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Generates visual prompts for each scene based on narrative keywords and mood."""
        logger.info("Generating cinematic visual prompts for image synthesis...")
        processed_scenes = []

        for scene in scenes:
            narration = scene["narration"]
            mood = scene.get("mood", "dramatic")
            style = self.STYLE_PRESETS.get(mood, self.STYLE_PRESETS["dramatic"])

            # Extract key concept from narration (first 15 words)
            core_concept = " ".join(narration.split()[:15])
            full_prompt = f"{core_concept}, {style}"

            data = scene.copy()
            data["visual_prompt"] = full_prompt
            data["negative_prompt"] = self.NEGATIVE_PROMPT
            processed_scenes.append(data)

        logger.info("Cinematic visual prompts successfully generated.")
        return processed_scenes
