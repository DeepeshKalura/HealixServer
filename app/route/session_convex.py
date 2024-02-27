import os
import sys
from datetime import datetime
from fastapi import APIRouter, HTTPException, status

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import database as db
import pre_processing as pp
from pydantic import BaseModel
from response import use_model, ChatGPTModel, user_input