import io
import pathlib
import subprocess
import streamlit as st
from pydub import AudioSegment

filename = None
filestream = io.BytesIO()

st.title('MP3 to WAV Converter test app')

st.markdown("""This is a quick example app for using the **pydub** audio library on Streamlit Cloud.
There are some issues with `ffmpeg` on Streamlit Cloud regarding temporary files and file permissions.
The quick fix is to use `libav` instead of `ffmpeg` in `packages.txt` file, because pydub prefers `libav` over `ffmpeg` if it is installed.
Therefore this example app uses `libav`.""")

uploaded_mp3_file = st.file_uploader('Upload Your MP3 File', type=['mp3', 'm4a'])

if uploaded_mp3_file:
    uploaded_mp3_file_length = len(uploaded_mp3_file.getvalue())
    if uploaded_mp3_file_length > 0:
        st.text(f'Size of uploaded mp3 file: {uploaded_mp3_file_length} bytes')
        audio_segment = AudioSegment.from_mp3(uploaded_mp3_file)
        # do some more processing here with the mp3 file(?)
        handler = audio_segment.export(filestream, format="wav")  # handler not needed
        filename = pathlib.Path(uploaded_mp3_file.name).stem

if filestream and filename:
    content = filestream.getvalue()
    length = len(content)
    if length > 0:
        st.download_button(label="Download wav file",
                data=content,
                file_name=f'{filename}.wav',
                mime='audio/wav')
        st.text(f'Size of "{filename}.wav" file to download: {length} bytes')