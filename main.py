# Steps to achieve
# User -> Real-time Audio Input -> Speech-to-Text (STT) -> Text Input -> AI Processing and Mapping -> AI-generated Text Response -> Text-to-Speech (TTS) -> Real-time Audio Output (spoken response)

# use for the import data from .env to the project
from dotenv import load_dotenv, find_dotenv
import os

# AssemblyAI

import assemblyai as aai

# Google docs

import pathlib
import textwrap
import google.generativeai as genai


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
# print(transcript.text)
# print("\n\n\n")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
modelGeminiPro = genai.GenerativeModel('gemini-pro')

messageString = transcript.text









# ! This is the great start i will going to first create the audio to the 

print("Currently here")  
response = modelGeminiPro.generate_content(messageString)
print("Reached here")
# print("Now Reached Here")
print(response.text)

