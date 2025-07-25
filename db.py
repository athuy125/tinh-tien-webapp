from config import MONGO_URI
from pymongo import MongoClient
from datetime import datetime
# 👉 Điền URI của bạn từ MongoDB Atlas


client = MongoClient(MONGO_URI)
db = client["athuy125"]           # Tên database
collection = db["atneverdie1"]         # Tên collection
def delete_history_item(username, hang, index):
    doc = collection.find_one({"username": username})
    if doc:
        data = doc.get("data", {})
        history = data.get("history", {})
        items = history.get(hang, [])
        if 0 <= index < len(items):
            removed = items.pop(index)
            history[hang] = items
            data["history"] = history
            collection.update_one({"username": username}, {"$set": {"data": data}})
            return removed
    return None

def delete_mat_hang(username, hang):
    doc = collection.find_one({"username": username})
    if doc:
        data = doc.get("data", {})
        history = data.get("history", {})
        if hang in history:
            del history[hang]
            data["history"] = history
            collection.update_one({"username": username}, {"$set": {"data": data}})

def save_data(username, data):
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
# ✅ Lưu dữ liệu tính toán
def save_tinh_toan(username, hang, content):
    doc = collection.find_one({"username": username})
    if doc:
        data = doc.get("data", {})
        history = data.get("history", {})
    else:
        data = {}
        history = {}

    if hang not in history:
        history[hang] = []
    history[hang].append(content)
    data["history"] = history

    collection.update_one(
        {"username": username},
        {"$set": {"data": data}},
        upsert=True
    )
# ✅ Lưu / cập nhật nợ
def save_debt(username, name, amount):
    db["debts"].update_one(
        {"username": username, "name": name},
        {"$set": {"amount": amount, "updated_at": datetime.now().isoformat()}},
        upsert=True
    )

# ✅ Lưu lịch sử (ví dụ: thêm ghi chú, tính toán, v.v)
def save_history(username, mat_hang, content):
    db["histories"].insert_one({
        "username": username,
        "mat_hang": mat_hang,
        "content": content,
        "created_at": datetime.now().isoformat()
    })

# ✅ Lấy lịch sử tính toán theo mặt hàng
def get_history(username, hang):
    doc = collection.find_one({"username": username})
    if doc:
        data = doc.get("data", {})
        history = data.get("history", {})
        return history.get(hang, [])
    else:
        return []
