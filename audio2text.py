from dotenv import load_dotenv
import os
import subprocess
import ffmpeg
import time
import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment
import warnings

# Suppress RuntimeWarnings related to ffprobe/avprobe
warnings.filterwarnings("ignore", category=RuntimeWarning, message="Couldn't find ffprobe or avprobe")


# Get Configuration Settings
load_dotenv()
cog_key = os.getenv('COG_SERVICE_KEY')
cog_region = os.getenv('COG_SERVICE_REGION')

def convert_audio_to_wav(input_file, output_file):
    subprocess.call(['ffmpeg', '-i', input_file, output_file], shell=True)


def speech_recognize_continuous_from_file(file):
    audio_file_path = os.path.abspath(file)
    speech_config = speechsdk.SpeechConfig(cog_key, cog_region)
    audio_input = speechsdk.audio.AudioConfig(filename=audio_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    return speech_recognizer

def transcribe_audio(input_audio_file):
    try:
        # Convert the input audio file to .wav
        output_audio_file = "output_audio.wav"
        convert_audio_to_wav(input_audio_file, output_audio_file)

        # Create the speech recognizer using the function
        speech_recognizer = speech_recognize_continuous_from_file(output_audio_file)

        # Define a callback function for recognized speech
        recognized_text = []  # Initialize an empty list to store recognized text

        def on_recognized(evt):
            result_text = evt.result.text
            sentences = result_text.split(".")
            text = ".\n".join(sentences)
            recognized_text.append(text)  # Append recognized text to the list

        # Subscribe to the recognized event
        speech_recognizer.recognized.connect(on_recognized)

        # Start continuous speech recognition
        speech_recognizer.start_continuous_recognition()

        # Wait for recognition to complete (adjust the duration as needed)
        time.sleep(20)  # This allows recognition to continue for 10 seconds

        # Stop continuous recognition
        speech_recognizer.stop_continuous_recognition()

        # Join the recognized text from the list into a single string
        final_recognized_text = "\n".join(recognized_text)

        # Return the recognized text
        return final_recognized_text

    except Exception as ex:
        return str(ex)

