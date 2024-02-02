import os
from openai import OpenAI
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv, find_dotenv
import requests

load_dotenv(find_dotenv())


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def audio(text):
    client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    ).write_to_file("audio.mp3")


def store_compound_score(sentence):
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(sentence)
    return vs["compound"]



def store_theme_of_user(sentence):
    api = os.getenv('HUGGINGFACE_AUTH_TOKEN')
    candidate_labels = ['Personal', 'Love', 'Work', 'Education','Technology']
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
    headers = {"Authorization": f"Bearer {api}"}
    payload = {
        "inputs": sentence,
        "parameters": {
            "candidate_labels": candidate_labels
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    user_them = {}
    for i in range(len(result["labels"])):
        
        label = result["labels"][i]
        score = result["scores"][i]
        user_them[label] = score

    return user_them

