from dotenv import load_dotenv
import os
from pathlib import Path
from playsound import playsound
import azure.cognitiveservices.speech as speech_sdk

def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        cog_key = os.getenv('COG_SERVICE_KEY')
        cog_region = os.getenv('COG_SERVICE_REGION')

        audio_file_path = Path("dream.wav").resolve()

        speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)
        audio_input = speech_sdk.AudioConfig(filename=str(audio_file_path))
        speech_recognizer = speech_sdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

        #playsound(audio_file_path)

        print("Recognizing first result...")

        result = speech_recognizer.recognize_once()
        
        if result.reason == speech_sdk.ResultReason.RecognizedSpeech:
            print('Recognized: {}'.format(result.text))
        elif result.reason == speech_sdk.ResultReason.NoMatch:
            print('No audio could be recognized: {}'.format(result.no_match_details))
        elif result.reason == speech_sdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print('Audio Recognition canceled: {}'.format(cancellation_details.reason))
            if cancellation_details.reason == speech_sdk.CancellationReason.Error:
                print('Error details: {}'.format(cancellation_details.error_details))

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()
