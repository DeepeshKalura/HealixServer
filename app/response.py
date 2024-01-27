import os
import openai
import requests
from abc import ABC, abstractmethod
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


client = openai.Client(api_key=os.getenv('OPENAI_API_KEY'))    

class Model(ABC):
    @abstractmethod
    def generate_response(self, message: str) -> str:
        pass


class ChatGPTModel(Model):
    def generate_response(self, message: str) -> str:
        pr = "You are a therapist in the world who helps patients remove their mental discomfort by communicating with them. Your communication is always the short question so patient can open there heart to you"
        response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": pr},
            {"role": "user", "content": message}
        ]
        )
        return response.choices[0].message.content

class GeminiModel(Model):
    def generate_response(message: str) -> str:
        url = "http://127.0.0.1:5000"
        response = requests.get(url+"/response", json={
            "message": message,
        })

        if(response.status_code == 200):
            output = response.json()["message"]
            return output
        print("Model have some issue")
        exit(2)


def use_model(model: Model, message: str) -> str:
    return model.generate_response(message)

gpt_model = ChatGPTModel()
message = "Hello, how are you?"
response_gpt = use_model(gpt_model, message)
print("Response from GPT:", response_gpt)