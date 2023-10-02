import subprocess

def convert_mp3_to_wav(input_file, output_file):
    """
    Convert an audio file from MP3 to WAV format using FFmpeg.

    Args:
        input_file (str): Path to the input MP3 file.
        output_file (str): Path to the output WAV file.

    Returns:
        bool: True if conversion is successful, False otherwise.
    """
    try:
        subprocess.call(['ffmpeg', '-i', input_file, output_file])
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# Define input and output file paths
input_audio_file = 'dream.m4a'
output_wav_file = 'converted_to_wav_file.wav'

# Call the conversion function
if convert_mp3_to_wav(input_audio_file, output_wav_file):
    print("Conversion successful.")
else:
    print("Conversion failed.")
