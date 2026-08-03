"""
MystoriumX AI Studio - End-to-End Master Pipeline Execution
"""
from pathlib import Path
from config import Config
from modules.audio_ducking import AudioDuckingEngine
from modules.image_engine import ImageEngine
from modules.music_engine import MusicEngine
from modules.prompt_generator import PromptGenerator
from modules.render_engine import RenderEngine
from modules.scene_detector import SceneDetector
from modules.script_engine import ScriptEngine
from modules.sfx_engine import SFXEngine
from modules.subtitle_engine import SubtitleEngine
from modules.video_engine import VideoEngine
from modules.voice_engine import VoiceEngine
from utils.file_manager import PipelineState
from utils.logger import setup_logger

logger = setup_logger("Pipeline")


class DocumentaryPipeline:
    """Orchestrates end-to-end automated documentary video creation pipeline."""

    def __init__(self, script_path: Path = Config.RAW_SCRIPT):
        Config.setup_directories()
        self.script_path = script_path
        self.state = PipelineState()

    def run(self):
        """Executes full generation sequence with stage state tracking and dynamic resuming."""
        logger.info("===============================================")
        logger.info("   MYSTORIUMX AI STUDIO - PIPELINE INITIALIZED  ")
        logger.info("===============================================")

        # Stage 1: Script Parsing
        if not self.state.is_completed("script_parsing"):
            script_eng = ScriptEngine(self.script_path)
            scenes = script_eng.load_and_parse()
            self.state.update_stage("script_parsing", scenes)
        else:
            scenes = self.state.get_stage_data("script_parsing")
            logger.info("Resuming: Loaded parsed script from pipeline state.")

        # Stage 2: Scene Mood Analysis
        if not self.state.is_completed("mood_detection"):
            detector = SceneDetector()
            scenes = detector.analyze_scenes(scenes)
            self.state.update_stage("mood_detection", scenes)
        else:
            scenes = self.state.get_stage_data("mood_detection")

        # Stage 3: Prompt Engineering
        if not self.state.is_completed("prompt_generation"):
            prompt_gen = PromptGenerator()
            scenes = prompt_gen.generate_prompts(scenes)
            self.state.update_stage("prompt_generation", scenes)
        else:
            scenes = self.state.get_stage_data("prompt_generation")

        # Stage 4: Voiceover Synthesis
        if not self.state.is_completed("voice_synthesis"):
            voice_eng = VoiceEngine()
            scenes = voice_eng.process_narration(scenes)
            self.state.update_stage("voice_synthesis", scenes)
        else:
            scenes = self.state.get_stage_data("voice_synthesis")

        # Stage 5: Image Assets Generation
        if not self.state.is_completed("image_generation"):
            image_eng = ImageEngine()
            scenes = image_eng.generate_images(scenes)
            self.state.update_stage("image_generation", scenes)
        else:
            scenes = self.state.get_stage_data("image_generation")

        # Stage 6: Video Scene Clips Assembly
        if not self.state.is_completed("video_clips"):
            video_eng = VideoEngine()
            scenes = video_eng.create_scene_clips(scenes)
            self.state.update_stage("video_clips", scenes)
        else:
            scenes = self.state.get_stage_data("video_clips")

        # Stage 7: Subtitle & Transcription Generation
        if not self.state.is_completed("subtitles"):
            sub_eng = SubtitleEngine()
            scenes = sub_eng.generate_subtitles(scenes)
            self.state.update_stage("subtitles", scenes)
        else:
            scenes = self.state.get_stage_data("subtitles")

        # Stage 8: Background Music & Audio Ducking
        if not self.state.is_completed("master_audio"):
            total_duration = sum(s.get("duration", 0.0) for s in scenes)
            music_eng = MusicEngine()
            bg_music_path = music_eng.generate_ambient_track(scenes, total_duration)

            sfx_eng = SFXEngine()
            scenes = sfx_eng.process_sfx(scenes)

            ducking_eng = AudioDuckingEngine()
            mastered_audio = ducking_eng.process_audio(scenes, bg_music_path)

            audio_data = {
                "mastered_audio_path": str(mastered_audio),
                "scenes": scenes,
            }
            self.state.update_stage("master_audio", audio_data)
        else:
            audio_data = self.state.get_stage_data("master_audio")
            mastered_audio = Path(audio_data["mastered_audio_path"])
            scenes = audio_data["scenes"]

        # Stage 9: Final Master Video Rendering
        if not self.state.is_completed("final_render"):
            renderer = RenderEngine()
            final_video_path = renderer.render_final_video(scenes, mastered_audio)
            self.state.update_stage("final_render", str(final_video_path))
        else:
            final_video_path = Path(self.state.get_stage_data("final_render"))

        logger.info("===============================================")
        logger.info(f" PIPELINE COMPLETE! OUTPUT: {final_video_path}")
        logger.info("===============================================")
        return final_video_path


if __name__ == "__main__":
    pipeline = DocumentaryPipeline()
    pipeline.run()
