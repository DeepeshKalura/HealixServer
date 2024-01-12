import random
import google.generativeai as gemini
import pandas as pd
import os
from dotenv import load_dotenv, find_dotenv


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'home/deepesh/.config/gcloud/application_default_credentials.json'

load_dotenv(find_dotenv())

gemini.configure(api_key=os.getenv("GEMINI_API_KEY"),

)

train_files = [f for f in os.listdir('/home/deepesh/development/challange/solution/textToSpeech/learn/chatmodel/Train') if f.endswith('.csv')]

train_data = pd.concat([pd.read_csv(f'/home/deepesh/development/challange/solution/textToSpeech/learn/chatmodel/Train/{f}') for f in train_files])
train_dic_data = train_data.to_dict('records')
def convert_data(train_dic_data):
    training_data = []
    for i in range(0, len(train_dic_data), 2):
        patient_dic = train_dic_data[i]
        therapist_dic = train_dic_data[i+1]
        if patient_dic['Type'] == 'P' and therapist_dic['Type'] == 'T':
            text_input = patient_dic['Utterance']
            output = therapist_dic['Utterance']
            training_data.append({'text_input': text_input, 'output': output})
    return training_data

training_data = convert_data(train_dic_data)
base_model = [
    m for m in gemini.list_models()
    if "createTunedTextModel" in m.supported_generation_methods][0]
base_model.name

for i, m in zip(range(5), gemini.list_tuned_models()):
  print(m.name)