import bcrypt
from pymongo import MongoClient

# MongoDB Atlas URI and database name
MONGO_URI = "mongodb+srv://admin:admin123789!@db-nida-pj.nychb0m.mongodb.net/"
MONGO_DB_NAME = "sample_mflix"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

# Create a new hashed password from plain text
plain_password = "12345678"
hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

# Update the user's password in the database
result = db.users.update_one(
    {"name": "user test"},  # Find user by name
    {"$set": {"password": hashed_password.decode('utf-8')}}  # Set the new hashed password
)

# Check the result of the update operation
if result.modified_count:
    print("Password updated successfully.")
else:
    print("User 'user test' not found or password was not changed.")
