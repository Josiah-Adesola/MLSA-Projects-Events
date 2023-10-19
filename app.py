import streamlit as st
import tempfile
import os

from audio2text import convert_audio_to_wav, transcribe_audio  # Replace with your module name

def main():
    st.title("Audio to Text Transcription")

    uploaded_audio = st.file_uploader("Upload an audio file (MP3, WAV, etc.)", type=["mp3", "wav", "m4a"])

    # Check if the uploaded audio is not None and not in WAV format
    if uploaded_audio is not None and not uploaded_audio.name.endswith(".wav"):
        # Save the uploaded audio to a temporary file and convert it to WAV
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(uploaded_audio.read())
            temp_audio_path = temp_audio.name

            # Convert the uploaded audio to WAV format
            convert_audio_to_wav(temp_audio_path, temp_audio_path)

        st.audio(temp_audio_path, format="audio/wav")

        if st.button("Transcribe"):
            with st.spinner("Transcribing..."):
                result = transcribe_audio(temp_audio_path)
                if result is not None:
                    st.write("Transcription Result:")
                    st.write(result)
                else:
                    st.write("Transcription failed or returned 'None'.")

        # Clean up the temporary audio file
        os.remove(temp_audio_path)
        
        # Clear the cache for the output.wav
        st.experimental_rerun()

if __name__ == "__main__":
    main()
