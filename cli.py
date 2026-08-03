"""
MystoriumX AI Studio - Command Line Interface (CLI)
"""
import argparse
from pathlib import Path
from config import Config
from pipeline import DocumentaryPipeline


def parse_args():
    parser = argparse.ArgumentParser(
        description="MystoriumX AI Studio - CLI Master Video Pipeline"
    )

    parser.add_argument(
        "--script",
        type=str,
        default=str(Config.RAW_SCRIPT),
        help="Path to the raw script text file (default: inputs/raw_script.txt)"
    )

    parser.add_argument(
        "--voice",
        type=str,
        default=Config.TTS_VOICE,
        help="Edge-TTS voice identifier (e.g. en-US-ChristopherNeural)"
    )

    parser.add_argument(
        "--whisper-model",
        type=str,
        default=Config.WHISPER_MODEL_SIZE,
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size for subtitle transcription"
    )

    parser.add_argument(
        "--reset-state",
        action="store_true",
        help="Clear previous pipeline state before executing"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # Override dynamic configuration flags
    Config.TTS_VOICE = args.voice
    Config.WHISPER_MODEL_SIZE = args.whisper_model

    script_path = Path(args.script)

    if args.reset_state:
        from utils.file_manager import PipelineState
        PipelineState().reset()
        print("Pipeline state cleared.")

    print(f"Starting MystoriumX AI Studio Pipeline with script: {script_path}")
    pipeline = DocumentaryPipeline(script_path=script_path)
    final_output = pipeline.run()

    print(f"\nPipeline Execution Finished Successfully!")
    print(f"Master Video saved at: {final_output}\n")


if __name__ == "__main__":
    main()
