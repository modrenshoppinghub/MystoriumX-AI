"""
MystoriumX AI Studio - Dynamic Audio Ducking Engine
"""

# --- Python 3.14 / Pydub Audioop Fix ---
try:
    import audioop
except ImportError:
    try:
        import audioop_lts as audioop
        import sys

        sys.modules["audioop"] = audioop
        sys.modules["pyaudioop"] = audioop
    except ImportError:
        pass
# ---------------------------------------

from pathlib import Path
import numpy as np
from pydub import AudioSegment
from utils.logger import setup_logger

logger = setup_logger("AudioDucking")


class AudioDuckingEngine:

    def __init__(
        self,
        voice_attenuation_db: float = -12.0,
        normal_bgm_db: float = -4.0,
        chunk_ms: int = 100,
    ):
        """
        :param voice_attenuation_db: وائس اوور کے دوران بیک گراؤنڈ میوزک جتنا کم کرنا ہے (dB میں)
        :param normal_bgm_db: عام حالات میں بیک گراؤنڈ میوزک کا والیوم
        :param chunk_ms: آڈیو پروسیسنگ کے لیے چنک کا سائز (ملٹی سیکنڈز)
        """
        self.voice_attenuation_db = voice_attenuation_db
        self.normal_bgm_db = normal_bgm_db
        self.chunk_ms = chunk_ms

    def process_ducking(
        self, voice_path: Path, bgm_path: Path, output_path: Path
    ) -> Path:
        """وائس اوور کی موجودگی کا پتہ لگا کر بیک گراؤنڈ میوزک کا والیوم آٹو ایڈجسٹ کرتا ہے"""
        logger.info(
            f"Applying dynamic audio ducking: {voice_path.name} + {bgm_path.name}"
        )

        try:
            voice_audio = AudioSegment.from_file(voice_path)
            bgm_audio = AudioSegment.from_file(bgm_path)
        except Exception as e:
            logger.error(f"Failed to load audio files: {e}")
            raise e

        # میوزک کی لمبائی کو وائس اوور کے برابر یا لوپ کرنا
        if len(bgm_audio) < len(voice_audio):
            loop_count = int(np.ceil(len(voice_audio) / len(bgm_audio)))
            bgm_audio = bgm_audio * loop_count

        bgm_audio = bgm_audio[: len(voice_audio)]
        bgm_audio = bgm_audio + self.normal_bgm_db

        # ڈائنامک ڈکنگ پروسیسنگ
        processed_bgm = AudioSegment.empty()
        silence_threshold = voice_audio.dBFS - 16

        for i in range(0, len(voice_audio), self.chunk_ms):
            voice_chunk = voice_audio[i : i + self.chunk_ms]
            bgm_chunk = bgm_audio[i : i + self.chunk_ms]

            # اگر آواز خاموشی کی حد سے زیادہ ہو تو میوزک کا والیوم کم کریں
            if voice_chunk.dBFS > silence_threshold:
                ducked_chunk = bgm_chunk + self.voice_attenuation_db
                processed_bgm += ducked_chunk
            else:
                processed_bgm += bgm_chunk

        # وائس اوور اور پروسیس شدہ بیک گراؤنڈ میوزک کو مکس کریں
        final_mixed_audio = voice_audio.overlay(processed_bgm)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        final_mixed_audio.export(output_path, format="mp3")

        logger.info(f"Audio ducking complete. Output saved to: {output_path}")
        return output_path
