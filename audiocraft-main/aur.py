import streamlit as st
import torchaudio
import os
import time
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

# Set page config first
st.set_page_config(page_title="Auralis", page_icon="🎵")

# Load model
@st.cache_resource
def load_model():
    return MusicGen.get_pretrained("facebook/musicgen-small")

model = load_model()

def generate_music(prompt, duration):
    model.set_generation_params(duration=duration)
    st.info("Generating music...")
    progress = st.progress(0)
    start_time = time.time()
    for i in range(10):
        time.sleep(0.3)
        progress.progress((i + 1) / 10)
    wav = model.generate([prompt])
    progress.empty()
    audio_path = f"generated/generated_{int(time.time())}.wav"
    audio_write(audio_path.replace(".wav", ""), wav[0].cpu(), model.sample_rate, strategy="loudness")
    return audio_path

def play_predefined(track_name, file_path):
    st.info(f"Loading '{track_name}'...")
    time.sleep(5)
    if os.path.exists(file_path):
        st.audio(file_path, format="audio/mp3")
        with open(file_path, "rb") as f:
            st.download_button(f"⬇ Download {track_name}", f, file_name=f"{track_name}.mp3")
    else:
        st.error(f"{track_name} track not found at {file_path}")

def app():
    st.title("🎵 Auralis")
    st.markdown("Welcome to **Auralis** — The New Age Music Generation Companion.")

    choice = st.selectbox("Choose what you want to do", ["Generate Music", "Play Predefined Track"])

    if choice == "Generate Music":
        prompt = st.text_input("Enter a music prompt:", "")
        duration = st.slider("Select duration (seconds)", 10, 30, 20, step=10)
        if st.button("Generate"):
            if prompt.strip() == "":
                st.warning("Please enter a prompt to generate music.")
            else:
                audio_file = generate_music(prompt, duration)
                st.success("Music generated successfully!")
                st.audio(audio_file)
                with open(audio_file, "rb") as f:
                    st.download_button("⬇ Download Generated Music", f, file_name="auralis_output.wav")

    elif choice == "Play Predefined Track":
        predefined = st.selectbox("Choose a track", [
            "Matushka (Phonk Version)",
            "Motherboard (Drum Version)",
            "Veridis Quo (Soft Version)"
        ])
        if st.button("Play Track"):
            if "Matushka" in predefined:
                play_predefined("Matushka", "tracks/matushka.mp3")
            elif "Motherboard" in predefined:
                play_predefined("Motherboard", "tracks/motherboard.mp3")
            elif "Veridis Quo" in predefined:
                play_predefined("Veridis Quo", "tracks/veridis_quo.mp3")

if __name__ == "__main__":
    app()
