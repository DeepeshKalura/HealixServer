import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())



client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def audio(text):
    client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    ).write_to_file("audio.mp3")


