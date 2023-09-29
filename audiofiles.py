from dotenv import load_dotenv
import os
import time
from playsound import playsound
import azure.cognitiveservices.speech as speechsdk


# Get Configuration Settings
load_dotenv()
cog_key = os.getenv('COG_SERVICE_KEY')
cog_region = os.getenv('COG_SERVICE_REGION')

def speech_recognize_continuous_from_file(file):
    audio_file_path = os.path.abspath(file)
    speech_config = speechsdk.SpeechConfig(cog_key, cog_region)
    audio_input = speechsdk.audio.AudioConfig(filename=audio_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    return speech_recognizer

def main():
    try:
        # Create the speech recognizer using the function
        audio_file = "dream.wav"
        speech_recognizer = speech_recognize_continuous_from_file(audio_file)
        # playsound(audio_file)

        # Define a callback function for recognized speech
        def on_recognized(evt):
            return "{}".format(evt.result.text)

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
        input("Press Enter to stop recognition...")

        # Stop continuous recognition
        speech_recognizer.stop_continuous_recognition()

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
