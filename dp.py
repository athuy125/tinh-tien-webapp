# db.py
from pymongo import MongoClient
from datetime import datetime
# 👉 Điền URI của bạn từ MongoDB Atlas
MONGO_URI = "mongodb+srv://<db_username>:<db_password>@cluster0.sjcwtjn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client["athuy125"]           # Tên database
collection = db["atneverdie1"]         # Tên collection

def save_data(username, data):
    """
    Lưu data (kiểu dict) của 1 user theo username.
    """
    collection.update_one(
        {"username": username},
        {"$set": {"data": data}},
        upsert=True
    )

def load_data(username):
    """
    Lấy data (kiểu dict) của 1 user theo username.
    """
    doc = collection.find_one({"username": username})
    if doc:
        return doc.get("data", {})
    else:
        return {}
