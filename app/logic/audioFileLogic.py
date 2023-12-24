# Steps to achieve
# User -> Real-time Audio Input -> Speech-to-Text (STT) -> Text Input -> AI Processing and Mapping -> AI-generated Text Response -> Text-to-Speech (TTS) -> Real-time Audio Output (spoken response)

# use for the import data from .env to the project
from dotenv import load_dotenv, find_dotenv
import os


# AssemblyAI --> Speech-to-Text (STT)

import assemblyai as aai

# Google docs  --> Main AI bot


# Speech To text  --> Speech-to-Text (STT)
from gtts import gTTS


firstChat = True



def audioFileProceesing(audio_file, chatWithModel):
    load_dotenv(find_dotenv())
    aai.settings.api_key = os.getenv("AAI_API_KEY")
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)



    input_message_string = transcript.text

    response = chatWithModel.Phykologist(input_message_string)  
    tts = gTTS(response, lang='en')
    # response_audio = io.BytesIO()
    # tts.save(response_audio)
    # response_audio.seek(0)

    tts.save("response.mp3");



    



