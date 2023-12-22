# Steps to achieve
# User -> Real-time Audio Input -> Speech-to-Text (STT) -> Text Input -> AI Processing and Mapping -> AI-generated Text Response -> Text-to-Speech (TTS) -> Real-time Audio Output (spoken response)

# use for the import data from .env to the project
from dotenv import load_dotenv, find_dotenv
import os

# AssemblyAI --> Speech-to-Text (STT)

import assemblyai as aai

# Google docs  --> Main AI bot

import google.generativeai as genai

# Speech To text  --> Speech-to-Text (STT)
from gtts import gTTS



load_dotenv(find_dotenv())

aai.settings.api_key = os.getenv("AAI_API_KEY")
transcriber = aai.Transcriber()
# audioPath = ["HindiGretting.mp3","EnglishGretting.mp3"];
# audioFile = "HindiGretting.mp3";
# audioFile = "EnglishGretting.mp3";
audioFile = "professionalLength.mp3";
print("I am here");



# for audioFile in audioPath:

transcript = transcriber.transcribe(audioFile)
# print("Reached here")
# print(transcript.t generate(text="Hello there!", voice=voices[0])ext)
# print("\n\n\n")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
modelGeminiPro = genai.GenerativeModel('gemini-pro', generation_config=genai.GenerationConfig(max_output_tokens=100))

messageString = transcript.text

tts = gTTS(messageString, lang='en')



