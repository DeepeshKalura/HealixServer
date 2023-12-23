# It is very slow let me be honest here

import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
print(TTS().list_models())

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

messageString = "Hello world, My name is Deepesh Kalura!"

tts.tts_to_file(text=messageString, speaker_wav="record_out.wav", language="en", file_path="output.wav")