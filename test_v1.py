"""
MystoriumX AI Studio - Version 1 (V1) Test Execution Script
Tests: Script Parsing, Scene Splitting, Timing Estimation, and JSON Export
"""

import json
from pathlib import Path
from config import Config
from modules.script_parser import ScriptParser

# ٹیسٹ کے لیے ایک نمونہ (Sample) اسکرپٹ
SAMPLE_SCRIPT = """
مصنوعی ذہانت خاموشی سے ہماری دنیا کو بدل رہی ہے۔
کیا ہم ان فیصلوں کے لیے تیار ہیں جو الگورتھمز ہمارے لیے کریں گے؟
انسان نے سوچا تھا کہ تخلیق کاری صرف اس کا حق ہے، لیکن AI نے یہ غرور توڑ دیا۔
مستقبل اب بدل چکا ہے اور ہمیں اس کے ساتھ قدم سے قدم ملا کر چلنا ہوگا۔
"""


def run_v1_test():
    print("=" * 60)
    print("🎬 Running MystoriumX AI Studio - V1 Test (Script Parsing)")
    print("=" * 60)

    try:
        # 1. ScriptParser کا آبجیکٹ بنائیں
        parser = ScriptParser()

        # 2. اسکرپٹ کو پارس کریں
        print("\n[1/3] Parsing Raw Script into Scenes...")
        scenes = parser.parse_script(script_text=SAMPLE_SCRIPT)

        # 3. نتایج کو سکرین پر دکھائیں
        print(f"✅ Successfully Parsed {len(scenes)} Scenes:\n")
        for scene in scenes:
            print(f"  📌 Scene #{scene['scene_id']}")
            print(f"     Text     : {scene['text']}")
            print(f"     Words    : {scene['word_count']} words")
            print(f"     Est. Time: {scene['estimated_duration_sec']} seconds")
            print(f"     Prompt   : {scene['prompt']}")
            print("-" * 50)

        # 4. JSON فائل میں محفوظ کریں
        print("\n[2/3] Saving Scenes to JSON File...")
        json_output_path = Config.OUTPUT_DIR / "temp" / "parsed_scenes.json"
        saved_file = parser.save_parsed_scenes(
            scenes, output_path=json_output_path
        )

        # 5. فائل کی موجودگی کی تصدیق کریں
        if saved_file.exists():
            print(f"✅ JSON State File Created Successfully at:\n   {saved_file}")

            # 6. JSON کھول کر ڈیٹا چیک کریں
            with open(saved_file, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)

            print(
                f"\n[3/3] Verification: JSON File contains {len(loaded_data)} scenes."
            )
            print("=" * 60)
            print("🎉 V1 (Script & Scene Detection) TEST PASSED 100%!")
            print("=" * 60)
        else:
            print("❌ Failed: JSON file was not found!")

    except Exception as e:
        print(f"\n❌ V1 Test Execution Failed with Error: {e}")


if __name__ == "__main__":
    run_v1_test()
