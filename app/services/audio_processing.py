from google.cloud import speech
import wave
import os
from pydub import AudioSegment

from pydub import AudioSegment

def convert_to_16bit(input_file, output_file):
    """
    Converts the input WAV file to 16-bit depth and saves it as the output file.
    """
    try:
        # Load the original audio file
        audio = AudioSegment.from_wav(input_file)

        # Convert to 16-bit by setting the sample width to 2 bytes (16 bits)
        audio = audio.set_sample_width(2)  # 2 bytes = 16 bits

        # Export the file with the correct format
        audio.export(output_file, format="wav")
        print(f"File converted and saved as {output_file}")
    except Exception as e:
        print(f"Error converting audio: {e}")


def change_audio(file_path):
    """
    Adjust the audio file to 16kHz if required.
    """
    audio = AudioSegment.from_file(file_path)
    # Resample to 16kHz and convert to mono
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio = audio.set_sample_width(2)  # 2 bytes = 16 bits
    processed_file = "processed.wav"
    audio.export(processed_file, format="wav")
    return processed_file


async def process_audio(file_path, num_speakers=2):
    """
    Transcribes an audio file and performs speaker diarization.
    
    Args:
        audio_file (str): Path to the audio file.
        key_file (str): Path to the Google Cloud service account JSON key.
        num_speakers (int): Number of speakers in the audio.

    Returns:
        dict: Transcript with speaker labels and text.
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-key.json"
    audio_file = change_audio(file_path)

    client = speech.SpeechClient()

    # Load the audio file
    with open(audio_file, "rb") as audio:
        content = audio.read()

    audio = speech.RecognitionAudio(content=content)

    # Configure the request
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        diarization_config=speech.SpeakerDiarizationConfig(
            enable_speaker_diarization=True,
            min_speaker_count=num_speakers,
            max_speaker_count=num_speakers,
        ),
    )

    # Transcribe audio
    response = client.recognize(config=config, audio=audio)

    # Parse response
    result = response.results[-1]  # Diarization info is in the last result
    words = result.alternatives[0].words

    # Assign speaker labels
    transcript = []
    speaker_map = {1: "Patient", 2: "Doctor"}  # Map speaker IDs to roles
    current_speaker = words[0].speaker_tag
    current_text = []

    for word_info in words:
        if word_info.speaker_tag != current_speaker:
            # Save the current speaker's text
            transcript.append({
                "speaker": speaker_map.get(current_speaker, f"Speaker {current_speaker}"),
                "text": " ".join(current_text),
            })
            # Switch to the new speaker
            current_speaker = word_info.speaker_tag
            current_text = []

        current_text.append(word_info.word)

    # Append the final speaker's text
    transcript.append({
        "speaker": speaker_map.get(current_speaker, f"Speaker {current_speaker}"),
        "text": " ".join(current_text),
    })

    return transcript