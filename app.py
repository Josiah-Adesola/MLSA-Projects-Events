import streamlit as st

def main():
    st.title("Audio Input App")

    # Upload an audio file
    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg"])

    if audio_file is not None:
        st.audio(audio_file, format="audio/wav")

if __name__ == "__main__":
    main()
