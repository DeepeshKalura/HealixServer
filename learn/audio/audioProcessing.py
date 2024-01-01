import pyaudio
import wave
import numpy as np

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK_SIZE = 1024
THRESHOLD = 0.01  # Adjust this threshold based on your environment and microphone sensitivity
SILENCE_FRAMES_THRESHOLD = 3

# Global variables
silence_counter = 0

def record_audio(file_name, threshold=THRESHOLD, silence_frames_threshold=SILENCE_FRAMES_THRESHOLD):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK_SIZE)

    print("Recording...")

    frames = []
    is_talking = False

    while True:
        data = stream.read(CHUNK_SIZE)
        frames.append(data)

        # Convert binary data to numpy array
        audio_np = np.frombuffer(data, dtype=np.int16)

        # Check if the audio level exceeds the threshold
        if np.max(np.abs(audio_np)) > threshold:
            is_talking = True
            silence_counter = 0
        else:
            if is_talking:
                silence_counter += 1

            # If silence threshold is reached, stop recording
            if silence_counter >= silence_frames_threshold:
                print("Silence detected. Stopping recording.")
                break

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(file_name, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

if __name__ == "__main__":
    file_name = "new_recording.wav"
    record_audio(file_name)
