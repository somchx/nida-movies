import bcrypt
from pymongo import MongoClient

# MongoDB Atlas URI และชื่อ Database
MONGO_URI = "mongodb+srv://admin:admin123789!@db-nida-pj.nychb0m.mongodb.net/"
MONGO_DB_NAME = "sample_mflix"

# เชื่อมต่อ MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

# สร้างรหัสผ่านใหม่แบบ hash
plain_password = "12345678"
hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

result = db.users.update_one(
    {"name": "user test"},
    {"$set": {"password": hashed_password.decode('utf-8')}}
)

# ตรวจสอบผลลัพธ์
if result.modified_count:
    print("✅ อัปเดต password สำเร็จแล้ว")
else:
    print("❌ ไม่พบผู้ใช้ชื่อ 'test' หรือ password ไม่เปลี่ยน")
