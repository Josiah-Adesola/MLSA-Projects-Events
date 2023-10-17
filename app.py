import streamlit as st
import os
import tempfile
from audio2text import transcribe_audio

def main():
    st.title("Audio to Text Transcription")

    # Use a constant filename for the output_audio.wav
    output_audio_filename = "output_audio.wav"
    output_audio_path = os.path.join(tempfile.gettempdir(), output_audio_filename)

    uploaded_audio = st.file_uploader("Upload an audio file (MP3, WAV, m4a, etc.)", type=["mp3", "wav", "m4a"])

    if uploaded_audio is not None:
        # Save the uploaded audio to the output_audio.wav file
        with open(output_audio_path, "wb") as output_audio_file:
            output_audio_file.write(uploaded_audio.read())

        st.audio(output_audio_path, format="audio/wav")

        if st.button("Transcribe"):
            with st.spinner("Transcribing..."):
                result = transcribe_audio(output_audio_path)
                if result is not None:
                    st.write("Transcription Result:")
                    st.success(result)
                else:
                    st.write("Transcription failed or returned 'None'.")

if __name__ == "__main__":
    main()
