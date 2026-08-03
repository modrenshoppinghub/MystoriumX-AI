# 🎬 MystoriumX AI Studio

**MystoriumX AI Studio** is an automated, end-to-end documentary video generation engine designed for faceless channels, automated storytelling, and cinematic media creation.

---

## 🚀 Key Features

* **Script Engine & Parser:** Dynamically cleans and splits raw script files into structured scene blocks.
* **Scene Mood Detection:** Categorizes narrations into cinematic tones (`mysterious`, `dramatic`, `inspirational`, `suspenseful`).
* **Visual Prompt Engine:** Auto-generates high-end cinematic photorealistic Stable Diffusion / Midjourney prompts.
* **TTS Voice Engine:** Synthesizes natural narrations using `edge-tts`.
* **Subtitle Transcription:** Uses OpenAI's Whisper model to build frame-accurate SRT subtitle tracks.
* **Dynamic Audio Ducking:** Automatically lowers background music levels when narration is active.
* **Ken Burns & Video Renderer:** Assembles video clips, handles crossfade transitions, and exports full HD 1080p MP4s.
* **Pipeline State Persistence:** Supports resuming interrupted runs without re-rendering completed stages.
* **Dual Interface:** Interactive Web GUI powered by **Streamlit** alongside a full-featured **CLI**.

---

## 🛠️ Installation & Setup

### 1. Prerequisites
* Python **3.9+**
* FFmpeg installed and added to PATH

### 2. Clone Repository & Setup Environment
```bash
git clone [https://github.com/your-username/MystoriumX-AI-Studio.git](https://github.com/your-username/MystoriumX-AI-Studio.git)
cd MystoriumX-AI-Studio

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
