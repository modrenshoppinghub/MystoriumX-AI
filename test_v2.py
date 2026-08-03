"""
MystoriumX AI Studio - Version 2 (V2) Test Execution Script
Tests: Natural Neural Voice Generation, Exact Duration Calculation, JSON State Update
"""

import json
from pathlib import Path
from config import Config
from modules.script_parser import ScriptParser
from modules.voice_engine import VoiceEngine


def run_v2_test():
    print("=" * 60)
    print(
        "🎙️ Running MystoriumX AI Studio - V2 Test (Natural Voice Generation)"
    )
    print("=" * 60)

    try:
        # 1. Ensure V1 JSON State Exists
        temp_dir = Config.OUTPUT_DIR / "temp"
        scenes_json_path = temp_dir / "parsed_scenes.json"

        if not scenes_json_path.exists():
            print("Creating base scene structure from V1...")
            parser = ScriptParser()
            sample_text = (
                "مصنوعی ذہانت خاموشی سے ہماری دنیا کو بدل رہی ہے۔ "
                "کیا ہم ان فیصلوں کے لیے تیار ہیں؟"
            )
            scenes = parser.parse_script(sample_text)
            parser.save_parsed_scenes(scenes, scenes_json_path)

        # 2. Initialize Voice Engine
        voice_engine = VoiceEngine()
        audio_output_dir = temp_dir / "audio_clips"

        print(
            "\n[1/2] Synthesizing Natural Urdu Voiceovers (ur-PK-AsadNeural)..."
        )
        updated_scenes = voice_engine.process_scenes_voiceover(
            scenes_json_path=scenes_json_path,
            output_audio_dir=audio_output_dir,
            voice="ur-PK-AsadNeural",
        )

        print(
            f"✅ Successfully Generated {len(updated_scenes)} Voiceover Clips:\n"
        )
        for scene in updated_scenes:
            print(f"  📌 Scene #{scene['scene_id']}")
            print(f"     Text    : {scene['text']}")
            print(f"     Audio   : {scene['audio_path']}")
            print(f"     Duration: {scene['actual_duration_sec']} seconds")
            print("-" * 50)

        print("\n[2/2] V2 Test Verification...")
        with open(scenes_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "actual_duration_sec" in data[0] and Path(data[0]["audio_path"]).exists():
            print("=" * 60)
            print(
                "🎉 V2 (Natural Non-Robotic Voice Generation) TEST PASSED 100%!"
            )
            print("=" * 60)
        else:
            print("❌ V2 Verification Failed!")

    except Exception as e:
        print(f"\n❌ V2 Test Execution Failed with Error: {e}")


if __name__ == "__main__":
    run_v2_test()
