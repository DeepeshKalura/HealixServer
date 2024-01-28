import os
from openai import OpenAI
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())




classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
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
    candidate_labels = ['Personal', 'Love', 'Work', 'Education','Technology']
    result = classifier(sentence, candidate_labels)
    user_them = {}
    for i in range(len(result["labels"])):
        
        label = result["labels"][i]
        score = result["scores"][i]
        user_them[label] = score

    return user_them
    