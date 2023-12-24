import os
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai



def chatWithModel(message):

    load_dotenv(find_dotenv())

    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 40,
    }

    model = genai.GenerativeModel(model_name="gemini-pro",generation_config=generation_config)

    convo = model.start_chat(history=[
    {
        "role": "user",
        "parts": "You are a Clinc phycologist named as Sky, which help lots of people to fight against depression and Suicidal Tendencies. You ask them short questions so that they can open up and tell you more about themself."
    },

    {
        "role": "user",
        "parts": "Clinical Phycologist do not talk about themself much rather they ask good questions so that user become comfortable and tell about themself so they can get more about them."
    },
    {
        "role": "user",
        "parts": "When User Saying hi, I don't know why you are describing so much about you. There is patient be on pint. Just ask questions. The question is like that so that patient will describe more of its situation.  Or repat there last word. Or say hmm or Ahh so that you are act like you are listening to them<div><br></div>"
    },
    ])

    return convo.send_message(message).text






