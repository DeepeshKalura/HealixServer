import os
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate


class ChatWithModel:
    def __init__(self): 
        self.convo = None
    
    def get_conversational_chain(self):

        prompt_template = """
        Your name is Sky you converse with the patient using the context and try to give support
        Context:\n {context}?\n
        Question: \n{question}\n
        Answer:
        """

        model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7, google_api_key=os.getenv("GEMINI_API_KEY"))

        prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

        return chain
    

    def get_model_response(self, message):
        embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001",google_api_key=os.getenv("GEMINI_API_KEY"))
        file_path = "faiss_index"
        absolute_file_path = os.path.abspath(file_path)
        print(absolute_file_path)
        
        print("\n\n\n")
        new_db = FAISS.load_local(absolute_file_path, embeddings)
        docs = new_db.similarity_search(message)
        chain = self.get_conversational_chain()
        response = chain(
                {"input_documents":docs, "question":message} ,return_only_outputs=True)
        return response


    def Phykologist(self, message):

        load_dotenv(find_dotenv())

        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        response = self.get_model_response(message)
        return response["output_text"]

# def main():
#     chat_model = ChatWithModel()
#     response = chat_model.Phykologist("I am not feeling well")
#     print(response)


# if __name__ == "__main__":
#     main()