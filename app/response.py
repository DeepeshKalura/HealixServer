import os
import openai
import requests
from abc import ABC, abstractmethod
from dotenv import load_dotenv, find_dotenv
import requests
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

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

def get_conversational_chain(user_question, results):

    PROMPT_TEMPLATE = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n


    Answer the question based on the above context: {question}
    """

    context_text = results
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=user_question)
    

    return prompt

def user_input(user_question: str):
    embeddings = OpenAIEmbeddings()

    new_db = FAISS.load_local("faiss_index", embeddings)
    result = new_db.similarity_search(user_question)

    promot = get_conversational_chain(user_question=user_question, results=result)

    model = ChatOpenAI()
    response = model.predict(promot)

    return response


