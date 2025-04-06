from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS
import config

app = Flask(__name__)
CORS(app)

client = MongoClient(config.MONGO_URI)
db = client[config.MONGO_DB_NAME]

app.db = db

from app import api, view
