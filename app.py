"""
MystoriumX AI Studio - Main Streamlit Dashboard
"""

from pathlib import Path
import streamlit as st

from config import Config
from pipeline import DocumentaryPipeline

# Page Setup
st.set_page_config(
    page_title="MystoriumX AI Studio",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 MystoriumX AI Studio - Video & Voice Generator")
st.markdown("---")

# Sidebar - Settings
st.sidebar.header("⚙️ Video Settings")
voice_option = st.sidebar.selectbox(
    "🎙️ Select AI Voice Accent:",
    options=[
        "ur-PK-AsadNeural",        # Urdu Male (Natural)
        "ur-PK-UzmaNeural",        # Urdu Female (Natural)
        "en-US-ChristopherNeural", # English Male (Documentary)
        "en-US-JennyNeural",       # English Female
    ],
    index=0,
)

# Fetch Default Script if exists
default_script = ""
if hasattr(Config, "RAW_SCRIPT") and Config.RAW_SCRIPT.exists():
    try:
        with open(Config.RAW_SCRIPT, "r", encoding="utf-8") as f:
            default_script = f.read()
    except Exception:
        pass

# Script Input Area
st.subheader("📝 Enter Script Text")
script_text = st.text_area(
    "پست کریں یا یہاں اپنا اسکرپٹ لکھیں:",
    value=default_script,
    height=250,
    placeholder="یہاں اپنا اردو یا انگلش اسکرپٹ لکھیں..."
)

# Action Button
if st.button("🚀 Generate Full Video & Voice", type="primary", use_container_width=True):
    if not script_text.strip():
        st.error("⚠️ برائے مہربانی ویڈیو بنانے کے لیے پہلے اسکرپٹ لکھیں!")
    else:
        with st.spinner("⏳ AI Voiceover، مناظر تیار کیے جا رہے ہیں اور ویڈیو رینڈر ہو رہی ہے..."):
            try:
                pipeline = DocumentaryPipeline()
                final_video_path = pipeline.run(
                    script_text=script_text,
                    voice=voice_option
                )

                if final_video_path and Path(final_video_path).exists():
                    st.balloons()
                    st.success("🎉 آپ کی ویڈیو اور آواز کامیابی سے تیار ہو چکی ہے!")

                    st.markdown("---")
                    st.subheader("📺 Video Player (پیش نظارہ)")
                    
                    # Display Video with Audio output directly in Streamlit
                    st.video(str(final_video_path))

                    # Download Button
                    with open(final_video_path, "rb") as file:
                        st.download_button(
                            label="📥 Download Video MP4",
                            data=file,
                            file_name="mystoriumx_documentary.mp4",
                            mime="video/mp4",
                            use_container_width=True
                        )
                else:
                    st.error("❌ ویڈیو کی فائل تیار نہیں ہو سکی، پاتھ غلط ہے۔")

            except Exception as e:
                st.error(f"❌ Pipeline Execution Failed: {str(e)}")
