"""
MystoriumX AI Studio - Image Generation Engine
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from config import Config
from utils.logger import setup_logger

logger = setup_logger("ImageEngine")


class ImageEngine:
    """Handles AI image generation or placeholder creation for scenes"""

    def __init__(self, provider: str = None):
        self.provider = provider or getattr(
            Config, "IMAGE_ENGINE_PROVIDER", "mock"
        )
        self.width = getattr(Config, "IMAGE_WIDTH", 1920)
        self.height = getattr(Config, "IMAGE_HEIGHT", 1080)

    def _create_placeholder(self, prompt: str, output_path: Path) -> Path:
        """Fallback method to generate a clean visual placeholder image"""
        img = Image.new("RGB", (self.width, self.height), color=(15, 23, 42))
        draw = ImageDraw.Draw(img)

        # Draw framing border
        draw.rectangle(
            [20, 20, self.width - 20, self.height - 20],
            outline=(56, 189, 248),
            width=5,
        )

        # Display text on image
        display_text = f"MystoriumX Scene:\n\n{prompt[:120]}..."
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None

        draw.text(
            (self.width // 2, self.height // 2),
            display_text,
            fill=(241, 245, 249),
            anchor="mm",
            font=font,
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path)
        logger.info(f"Created visual scene frame at: {output_path}")
        return output_path

    def generate_image(self, prompt: str, output_path: Path = None) -> Path:
        """Main entry point to generate image for a given script scene prompt"""
        if output_path is None:
            output_path = (
                getattr(Config, "TEMP_DIR", Path("./output/temp"))
                / "generated_scene.png"
            )

        output_path = Path(output_path)

        # Generate local high-res placeholder frame
        return self._create_placeholder(prompt, output_path)

    def create_image(self, *args, **kwargs) -> Path:
        """Alias method for backward compatibility"""
        return self.generate_image(*args, **kwargs)
