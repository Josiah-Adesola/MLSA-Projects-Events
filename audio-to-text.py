from dotenv import load_dotenv
import os
import re
import time
from playsound import playsound
import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment


# Get Configuration Settings
load_dotenv()
cog_key = os.getenv('COG_SERVICE_KEY')
cog_region = os.getenv('COG_SERVICE_REGION')

def convert_audio_to_wav(input_file, output_file):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format="wav")

def speech_recognize_continuous_from_file(file):
    audio_file_path = os.path.abspath(file)
    speech_config = speechsdk.SpeechConfig(cog_key, cog_region)
    audio_input = speechsdk.audio.AudioConfig(filename=audio_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    return speech_recognizer

def main():
    try: 
        # Convert the input audio file to .wav
        input_audio_file = "audio-files\poor-breathe.m4a"  # Replace with the path to your input audio file
        output_audio_file = "output_audio.wav"
        convert_audio_to_wav(input_audio_file, output_audio_file)
        # Create the speech recognizer using the function
        speech_recognizer = speech_recognize_continuous_from_file(output_audio_file )
        #playsound(output_audio_file)

        # Define a callback function for recognized speech
        def on_recognized(evt):
            recognized_text = evt.result.text
            sentences = recognized_text.split(".")
            text = ".\n".join(sentences)

            print(text)

        # Subscribe to the recognized event
        speech_recognizer.recognized.connect(on_recognized)

        # Define a callback function to stop recognition
        def stop_cb(evt):
            print('CLOSING on {}'.format(evt))
            speech_recognizer.stop_continuous_recognition()
            global done
            done = True

        # Subscribe to session stopped and canceled events to stop recognition
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        # Start continuous speech recognition
        speech_recognizer.start_continuous_recognition()

        # Wait for input to stop recognition
        print("Press Enter to stop recognition... ")
        print ("--------------------------")
        input("")

        # Stop continuous recognition
        speech_recognizer.stop_continuous_recognition()

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
