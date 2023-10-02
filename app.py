import streamlit as st
import os
import tempfile
from audio2text import transcribe_audio

def main():
    st.title("Audio to Text Transcription")

    uploaded_audio = st.file_uploader("Upload an audio file (MP3, WAV,m4a, etc.)", type=["mp3", "wav", "m4a"])

    if uploaded_audio is not None:
        # Save the uploaded audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(uploaded_audio.read())
            temp_audio_path = temp_audio.name

        st.audio(temp_audio_path, format="audio/wav")

        if st.button("Transcribe"):
            with st.spinner("Transcribing..."):
                result = transcribe_audio(temp_audio_path)
                if result is not None:
                    st.write("Transcription Result:")
                    st.success(result)
                else:
                    st.write("Transcription failed or returned 'None'.")


if __name__ == "__main__":
    main()
