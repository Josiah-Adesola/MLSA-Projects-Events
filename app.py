import streamlit as st
import os
import tempfile
import hashlib  # For generating unique file names
from audio2text import transcribe_audio

def main():
    st.title("Audio to Text Transcription")

    uploaded_audio = st.file_uploader("Upload an audio file (MP3, WAV, m4a, etc.)", type=["mp3", "wav", "m4a"])

    if uploaded_audio is not None:
        # Generate a unique file name based on the file's content
        file_hash = hashlib.md5(uploaded_audio.read()).hexdigest()
        temp_audio_path = os.path.join(tempfile.gettempdir(), f"{file_hash}.wav")

        # Save the uploaded audio to the unique temporary file
        with open(temp_audio_path, "wb") as temp_audio_file:
            temp_audio_file.write(uploaded_audio.read())

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
