from flask import Flask
from flask_cors import CORS
from config import db 

app = Flask(__name__)
CORS(app)

app.db = db  

from app import api, view  
