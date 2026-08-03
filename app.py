"""
MystoriumX AI Studio - Web User Interface (Streamlit)
"""
import streamlit as st
from pathlib import Path
from config import Config
from pipeline import DocumentaryPipeline
from utils.file_manager import PipelineState

st.set_page_config(
    page_title="MystoriumX AI Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎬 MystoriumX AI Studio - Automated Documentary Generator")
st.markdown("Automated AI pipeline for producing YouTube-ready documentary videos, narrations, ducked audio, and subtitles.")

# --- Sidebar Configuration ---
st.sidebar.header("⚙️ Pipeline Configuration")

voice_option = st.sidebar.selectbox(
    "Narrator Voice (Edge-TTS)",
    options=["en-US-ChristopherNeural", "en-US-GuyNeural", "en-GB-SoniaNeural"],
    index=0
)
Config.TTS_VOICE = voice_option

whisper_model = st.sidebar.selectbox(
    "Whisper Model Size",
    options=["tiny", "base", "small", "medium"],
    index=1
)
Config.WHISPER_MODEL_SIZE = whisper_model

resolution_option = st.sidebar.selectbox(
    "Export Resolution",
    options=["1080p (1920x1080)", "720p (1280x720)"],
    index=0
)
if "720p" in resolution_option:
    Config.RESOLUTION = (1280, 720)

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Reset Pipeline State"):
    state = PipelineState()
    state.reset()
    st.sidebar.success("Pipeline state cleared!")

# --- Main Workspace ---
tab1, tab2, tab3 = st.tabs(["📝 Script Input", "⚡ Pipeline Execution", "🍿 Output & Preview"])

with tab1:
    st.subheader("Documentary Script Input")
    
    # Read existing script if available
    default_script_text = ""
    if Config.RAW_SCRIPT.exists():
        with open(Config.RAW_SCRIPT, "r", encoding="utf-8") as f:
            default_script_text = f.read()

    script_input = st.text_area(
        "Enter raw text or script scenes below:",
        value=default_script_text,
        height=300
    )

    if st.button("💾 Save Script"):
        Config.RAW_SCRIPT.parent.mkdir(parents=True, exist_ok=True)
        with open(Config.RAW_SCRIPT, "w", encoding="utf-8") as f:
            f.write(script_input)
        st.success("Script updated successfully!")

with tab2:
    st.subheader("Run Master Generation Pipeline")
    st.info("Clicking the button below will start the 9-stage video synthesis pipeline.")

    if st.button("🚀 Start Production Pipeline", type="primary"):
        with st.spinner("Processing pipeline... Please check console logs for step-by-step progress."):
            try:
                pipeline = DocumentaryPipeline()
                final_video_path = pipeline.run()
                st.success(f"Production Complete! Master Video ready at: {final_video_path}")
            except Exception as e:
                st.error(f"Pipeline Execution Failed: {e}")

with tab3:
    st.subheader("Master Video Output & Subtitles")
    output_video = Config.FINAL_VIDEO_DIR / "final_documentary.mp4"
    output_srt = Config.SUBTITLE_DIR / "full_documentary.srt"

    col1, col2 = st.columns([2, 1])

    with col1:
        if output_video.exists():
            st.video(str(output_video))
            with open(output_video, "rb") as file:
                st.download_button(
                    label="📥 Download Master Video (.MP4)",
                    data=file,
                    file_name="final_documentary.mp4",
                    mime="video/mp4"
                )
        else:
            st.warning("No generated master video found. Run the pipeline first.")

    with col2:
        st.markdown("### Subtitles File (.SRT)")
        if output_srt.exists():
            with open(output_srt, "r", encoding="utf-8") as srt_file:
                srt_content = srt_file.read()
            st.text_area("Generated Transcript", value=srt_content, height=250)
            st.download_button(
                label="📥 Download Subtitles (.SRT)",
                data=srt_content,
                file_name="subtitles.srt",
                mime="text/plain"
            )
        else:
            st.info("Subtitles will appear here after rendering.")
