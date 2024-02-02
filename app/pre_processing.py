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
    try :

        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        print("\n\n\n\n")
        print(result)
        print("\n\n\n\n")

    except Exception as e:
        print(e)
        result = {'sequence': sentence, 'labels': ['Personal', 'Love', 'Education', 'Technology', 'Work'], 'scores': [0.5388193726539612, 0.4398689270019531, 0.01173669658601284, 0.006696830503642559, 0.0028781406581401825]}
    user_them = {}
    if 'labels' in result and 'scores' in result:
        for i in range(5):
            
            label = result["labels"][i]
            score = result["scores"][i]
            user_them[label] = score
    else:
        print("No the world")
    print("\n\n\n\n")
    print(user_them)
    print("\n\n\n\n")
    return user_them


