from pymongo import MongoClient
import certifi

MONGO_URI = "mongodb+srv://admin:admin123789!@db-nida-pj.nychb0m.mongodb.net/sample_mflix?retryWrites=true&w=majority"
MONGO_DB_NAME = "sample_mflix"

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client[MONGO_DB_NAME]
