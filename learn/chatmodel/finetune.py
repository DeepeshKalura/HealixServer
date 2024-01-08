import random
import google.generativeai as gemini
import pandas as pd

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

gemini.configure(api_key=os.getenv("GEMINI_API_KEY"))

train_files = [f for f in os.listdir('/home/deepesh/development/challange/solution/textToSpeech/learn/chatmodel/Train') if f.endswith('.csv')]

train_data = pd.concat([pd.read_csv(f'/home/deepesh/development/challange/solution/textToSpeech/learn/chatmodel/Train/{f}') for f in train_files])

train_data = train_data.to_dict('records')

base_model = [
    m for m in gemini.list_models()
    if "createTunedTextModel" in m.supported_generation_methods][0]
base_model.name




