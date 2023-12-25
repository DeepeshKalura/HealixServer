import sounddevice as sd
import soundfile as sf
import numpy as np

# Complete the part of audio recording and saving it to the file

duration = 5 # The thing i want the duration like until person take a pause the stream should be on
sample_rate = 44100 # No idea what is sample rate is

# Record audio
print("Recording... Speak into the microphone.") # --> This thing i don't have to in the future rahter i will get the bytes from the frontend

audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
sd.wait()


print("Recording complete.")

output_file = "recorded_audio.wav"
sf.write(output_file, audio_data, sample_rate)

# Recordd the auido with the help of stream

