import os
import openai
import requests
from abc import ABC, abstractmethod
from dotenv import load_dotenv, find_dotenv
import requests
load_dotenv(find_dotenv())


client = openai.Client(api_key=os.getenv('OPENAI_API_KEY'))    

class Model(ABC):
    @abstractmethod
    def generate_response(self, message: str) -> str:
        pass


class ChatGPTModel(Model):
    def generate_response(self, user_message: str) -> str:
        response = requests.post("https://healix-chatgpt-model.onrender.com/model", json= {
            "input_text" : user_message
        })

        # pr = "You are a therapist in the world who helps patients remove their mental discomfort by communicating with them. Your communication is always the short question so patient can open there heart to you"
        # response = client.chat.completions.create(
        # model="gpt-3.5-turbo-1106",
        # messages=[
        #     {"role": "system", "content": "You are a emotional support assistant, skilled in giving emotional support,your knowledge and assistance is limited to mental health support,Don't give response if it is not in the mental health context"},
        #     {"role": "user", "content": f"Check if user is asking for mental or emotional support {user_message} if yes provide that support if no then respond with this is not my ability try to engage user in conversation and if needed try to give CBT also"}
        # ]
        # )
        result = response.json()              
        return result["message"]

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
